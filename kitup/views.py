from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User

#  The models and forms for the kitup app.
from kitup.forms import UserForm, ProfileForm, UserLoginForm, MatchForm, UserUpdateForm, EmailPasswordRecovery, MatchParticipantReportForm
from kitup.models import Profile, Sport, MatchLocation, Match, MatchParticipant, MatchParticipantReport

# The main index page for the website.
def index(request):

    # Get the most rescent matches taking place.
    matches = Match.objects.order_by('-start_datetime')[:30]
    context_dictionary = {'matches': matches}

    # Obtain match data about the user.
    if request.user.is_authenticated:

        # Determine if the player is participating in any of these matches.
        user_matches = {}
        profile = Profile.objects.get(user=request.user)
        for match in matches:
            try:
                participant = MatchParticipant.objects.get(profile=profile, match=match)
                user_matches[match.id] = participant
            except MatchParticipant.DoesNotExist:
                continue

        # Add the matches that the user is participating within.
        context_dictionary['user_matches'] = user_matches    

    # Finally, render the index page.
    return render(request, 'kitup/index.html', context_dictionary)


# Invoked when the user wishes to register for the site.
def user_register(request):
    # Whether or not the user has registered for the site.
    registered = False

    # Check whether the user is submitting a registration form or not.
    if request.method == 'POST':

        # Create forms based on the POST request method.
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)  # Needed to add request.FILES for pictures to be added

        # Check that the forms are in fact valid.
        if user_form.is_valid() and profile_form.is_valid():

            # Save the user model to the database.
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.email = user_form.cleaned_data['confirm_email']
            user.save()

            # Save the profile form.
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()

            #text_success = "You have sucessfully registered! Click <a href="%s">here</a> to login and join the fun!" % reverse('kitup:user_login')

            registered = True
            #messages.success(request, text_success)
            return redirect(reverse('kitup:web_response'))
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    # Render the template using the forms.
    response = render(request, 'kitup/user_register.html',
                      {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
    return response

# Invoked when a user performs an action (report, sign up, kick, etc...).
def web_response(request):

    # Get the messages passed on from other views:
    storage = messages.get_messages(request)
    context_dictionary = {'message': storage}

    response = render(request, 'kitup/web_response.html', context_dictionary)
    return response


# Invoked when the user wishes to log into the site using their credentials.
def user_login(request):
    if request.method == 'POST':

        # Create a form based on the POST request.
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():

            # Get the username and the password and attempt to authenticate it.
            username = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            # If user is None, no account found. Otherwise, exists and check status.
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('kitup:index'))
                else:
                    messages.error(request, "Your KitUp account has been disabled")
                    return redirect(reverse('kitup:web_response'))
            else:
                print(f'Invalid login details: {username} {password}')
                messages.error(request, "Invalid username and/or password!")
                return render(request, 'kitup/user_login.html', {'user_login_form': user_login_form})

        else:
            print(user_login_form.errors)
    else:
        user_login_form = UserLoginForm()

    # Finally, render the response if the form is not being submitted.
    response = render(request, 'kitup/user_login.html', {'user_login_form': user_login_form})
    return response


# Define view for retrieving the users email for password reset
def password_reset(request):
    context_dictionary = {}

    context_dictionary['email_password_form'] = EmailPasswordRecovery

    response = render(request, 'kitup/password_reset_form.html', context_dictionary)
    return response


# Needs completed if e have time
def password_reset_done(request):
    context_dictionary = {}

    if request.method == 'POST':

        email_password_reset_form = UserUpdateForm(request.POST)
        if email_password_reset_form.is_valid():
            email = email_password_reset_form.cleaned_data['email']
            print(email)
            if User.objects.filter(email=email).exists():
                print("email exists")

    response = render(request, 'kitup/password_reset_form.html', context_dictionary)
    return response

# Invoked in the event the user wishes to log out.
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('kitup:index'))


# Used to recover the credentials of the user.
def user_recover(request):
    pass


# View the profile of the user. Displays current matches etc.
@login_required
def user_profile(request):
    try:
        context_dictionary = {}
        context_dictionary['user_update_form'] = UserUpdateForm

        profile = Profile.objects.get(user=request.user)

        user_meta_data = User.objects.get(username=request.user)
        matches_participants = MatchParticipant.objects.filter(profile=profile)
        matches = []
        for matches_participant in matches_participants:
            #print(matches_participant.match)
            match = Match.objects.get(name=matches_participant.match)
            matches.append(match)

        print(matches)
        context_dictionary['first_name'] = user_meta_data.first_name
        context_dictionary['last_name'] = user_meta_data.last_name
        context_dictionary['email'] = user_meta_data.email
        context_dictionary['rating'] = profile.rating
        if profile.profile_picture is not None:
            context_dictionary['profile_picture'] = profile.profile_picture
        else:
            context_dictionary['profile_picture'] = None
        context_dictionary['matches'] = matches

        #print(user_meta_data.Profile.strikes)
        response = render(request, 'kitup/user_profile.html', context_dictionary)
        return response

    except Profile.DoesNotExist:
        #return HttpResponse('Profile does not exist.')
        messages.error(request, "Profile does not exist.")
        return redirect(reverse('kitup:web_response'))

# Permits the viewing of another players profile.
def user_view_profile(request, user_id):
    pass


# Permits the user to edit / alter their settings.
@login_required
def user_settings(request):
    pass

# The match creation form.
@login_required
def match_create(request):

    match_form = None
    if request.method == 'POST':

        # If the form is valid, create a new match.
        match_form = MatchForm(request.POST)
        if match_form.is_valid():

            # Create a new instance of match.
            match = match_form.save(commit=False)
            match.sport = Sport.objects.get(id=match_form.cleaned_data['sport_id'])
            match.owner = request.user
            match.location = MatchLocation.objects.get(id=match_form.cleaned_data['location_id'])
            match.save()

            # Create an instance of the participant.
            participant = MatchParticipant(profile=Profile.objects.get(user=request.user), match=match)
            participant.save()

            # Redirect the user to the created match page.
            return redirect(reverse('kitup:match_view', kwargs={'match_id': match_id}))
        else:
            print(match_form.errors)
    else:
        match_form = MatchForm()

    # Defines creation attributes.
    context_dictionary = {
        'match_form': match_form,
        'match': None,
        'editing': False, 
    }

    # Render the match creation page.
    return render(request, 'kitup/match_settings.html', context_dictionary)

@login_required
def match_edit(request, match_id):

    # Get the match being edited.
    match = None
    try:
        match = Match.objects.get(id=match_id)
    except:
        return HttpResponse('The match does not exist.')

    # If posting, save changes made to the match.
    match_form = None
    if request.method == 'POST':
        match_form = MatchForm(request.POST, instance=match)
        if match_form.is_valid():
            match_form.save()
            return redirect(reverse('kitup:match_view', kwargs={'match_id': match.id}))
        else:
            print(match_form.errors)
    else:
        match_form = MatchForm(instance=match)
        match_form.fields['sport_id'].widget.attrs['readonly'] = True
        match_form.fields['sport_id'].widget.attrs['disabled'] = True
        match_form.fields['start_datetime'].widget.attrs['readonly'] = True
        match_form.fields['start_datetime'].widget.attrs['disabled'] = True
        match_form.fields['end_time'].widget.attrs['readonly'] = True
        match_form.fields['end_time'].widget.attrs['disabled'] = True
        match_form.fields['location_id'].widget.attrs['readonly'] = True
        match_form.fields['location_id'].widget.attrs['disabled'] = True

    # Defines edit status.
    context_dictionary = {
        'match_form': match_form,
        'match': match,
        'editing': True,
    }

    # Finally, render the match edit page.
    return render(request, 'kitup/match_settings.html', context_dictionary)

# The user attempts to join the match.
@login_required
def match_join(request, match_id):

    try:

        # The profile of the joining user and the match they're attempting to join.
        profile = Profile.objects.get(user=request.user)
        match = Match.objects.get(id=match_id)

        # Check that the match can be joined
        if match.is_in_past():
            #return HttpResponse('Match in the past, cannot join')
            messages.error(request, "Match in the past, cannot join")
            return redirect(reverse('kitup:web_response'))

        # Handle if they've already joined the match.
        participant = None
        if MatchParticipant.objects.filter(profile=profile).exists():

            # Check their request.
            participant = MatchParticipant.objects.get(profile=profile)
            if participant.accepted:
                #return HttpResponse('Already accepted')
                messages.warning(request, "Already accepted")
                return redirect(reverse('kitup:web_response'))
            else:
                #return HttpResponse('Awaiting Response')
                messages.warning(request, "Awaiting Response")
                return redirect(reverse('kitup:web_response'))

        # Determine if the user can directly join.
        accepted = True
        if match.private or match.sport.max_participants <= MatchParticipant.objects.filter(match=match, accepted=True).count():
            accepted = False

        # Finally, create the instance of participant.
        participant = MatchParticipant(profile=profile, match=match, accepted=accepted)
        participant.save()

    except Match.DoesNotExist:
        #return HttpResponse('Match does not exist.')
        messages.error(request, "Match does not exist")
        return redirect(reverse('kitup:web_response'))

    # An Should not reach this point.
    #return HttpResponse('Participation request made.')
    messages.success(request, "Participation request made.")
    return redirect(reverse('kitup:web_response'))

# The user is attempting to leave the match.
@login_required
def match_leave(request, match_id):

    try:

        # The match being left and the leaving profile.
        profile = Profile.objects.get(user=request.user)
        match = Match.objects.get(id=match_id)

        # If the match is in the past, prevent them from leaving.
        if match.is_in_past():
            #return HttpResponse('Failed to leave, match in the past.')
            messages.error(request, "Failed to leave, match in the past")
            return redirect(reverse('kitup:web_response'))

        # The match owner has deleted their match, return to index.
        if match.owner is request.user:
            match.delete()
            return redirect(reverse('kitup:index'))

        # If the player is a participant, delete their participation instance.
        if not MatchParticipant.objects.filter(profile=profile,match=match).exists():
            #return HttpResponse('You are not a participant')
            messages.error(request, "You are not a participant")
            return redirect(reverse('kitup:web_response'))
        participant = MatchParticipant(profile=profile,match=match)
        participant.delete()

    except Match.DoesNotExist:
        #return HttpResponse('Match does not exist.')
        messages.error(request, "Match does not exist")
        return redirect(reverse('kitup:web_response'))

    # Redirect them back to the match view page.
    return redirect(reverse('kitup:match_view', kwargs={'match_id': match.id}))

'''
# Permits the user to report the player for a variety of reasons.
@login_required
def match_report(request, match_id, reported_user_id):

    try:

        # Get the match for which the participant is being reported.
        match = Match.objects.get(id=match_id)

        # Check that the match is in the past.
        if not match.is_in_past():
            return HttpResponse('Match not in past, cannot report.')
        elif request.user.id is reported_user_id:
            return HttpResponse('You cannot report yourself')

        # Check that the reporting user is a participant.
        reporting_profile = Profile.objects.get(user=request.user)
        if not MatchParticipant.objects.filter(profile=reporting_profile, match=match).exists():
            return HttpResponse('Youre not a participant')
        reporting_participant = MatchParticipant.objects.get(profile=reporting_profile, match=match)
        if not reporting_participant.accepted:
            return HttpResponse('Cannot report, not part of the match.')

        # Check that the user participated in the match.
        reported_user = User.objects.get(id=reported_user_id)
        reported_profile = Profile.objects.get(user=reported_user)
        if not MatchParticipant.objects.filter(profile=reported_profile, match=match).exists():
            return HttpResponse('Reported user not part of the match.')
        reported_participant = MatchParticipant.objects.get(profile=reported_profile, match=match)
        if not reported_participant.accepted:
            return HttpResponse('Player did not participate in this match.')

        # Validate the form.
        report_form = MatchParticipantReportForm(request.POST)
        if not report_form.is_valid():
            return HttpResponse('Invalid form')

        # Finally, create and save the report.
        report = report_form.save(commit=False)
        report.reporting_user = request.user
        report.reported_user = reported_user
        report.save()

    except Match.DoesNotExist:
        return HttpResponse('Match not found')
    except User.DoesNotExist:
        return HttpResponse('User does not exist')

    return HttpResponse('Report successfully submitted')
'''

# A simplified means of reporting the participant.
@login_required
def match_report(request, participant_id):

    try:

        # Get the reported participant data.
        reported_participant = MatchParticipant.objects.get(id=participant_id)
        reported_profile = reported_participant.profile
        reported_user = reported_profile.user

        # Get the reporting users profile.
        reporting_profile = Profile.objects.get(user=request.user)
        reporting_participant = MatchParticipant.objects.get(profile=reporting_profile, match=reported_participant.match)

        # Check whether the participant can be reported.
        if reported_user is request.user:
            #return HttpResponse('You cannot report yourself')
            messages.error(request, "You cannot report yourself")
            return redirect(reverse('kitup:web_response'))
        elif not reporting_profile.accepted:
            #return HttpResponse('You were not part of this game')
            messages.error(request, "You were not part of this game")
            return redirect(reverse('kitup:web_response'))
        elif not reported_participant.accepted:
            #return HttpResponse('Reported participant not part of game')
            messages.success(request, "Reported participant not part of game")
            return redirect(reverse('kitup:web_response'))
        elif not match.is_in_past():
            #return HttpResponse('Match is not past')
            messages.error(request, "Match is not past")
            return redirect(reverse('kitup:web_response'))

        # Check that the user is not reporting them selves and the match is past.
        if not reported_participant.match.is_in_past():
            #return HttpResponse('Match not in past, cannot report.')
            messages.error(request, "Match not in past, cannot report")
            return redirect(reverse('kitup:web_response'))
        elif not reported_participant.accepted:
            #return HttpResponse('The user did not participate in this match')
            messages.error(request, "The user did not participate in this match")
            return redirect(reverse('kitup:web_response'))
        elif reported_participant.match.owner is request.user:
            #return HttpResponse('You cannot report yourself')
            messages.error(request, "You cannot report yourself")
            return redirect(reverse('kitup:web_response'))

        # Check that the form is valid.
        report_form = MatchParticipantReportForm(request.POST)
        if not report_form.is_valid():
            #return HttpResponse('Invalid form')
            messages.error(request, "Invalid form submitted")
            return redirect(reverse('kitup:web_response'))

        # Create and save the report.
        report = report_form.save(commit=False)
        report.reporting_user = request.user
        report.reported_user = reported_user
        report.save()

        # Increment the number of times the player is reported.
        reported_profile.reported = reported_profile.reported + 1
        reported_profile.save()

        # If player reported more than once, kick then.
        if reported_profile.reported >= 3:
            reported_user.is_active = False
            reported_user.save()

    except MatchParticipant.DoesNotExist:
        #return HttpResponse('Failed to identify the participants')
        messages.error(request, "Failed to identify the participants")
        return redirect(reverse('kitup:web_response'))

    #return HttpResponse('Report successfully submitted')
    messages.success(request, "Report Successfully submitted")
    return redirect(reverse('kitup:web_response'))

# Permits the owner to accept a user into the match in the event it is private.
@login_required
def match_accept(request, participant_id):
    
    try:

        # Get the participant that's to be accepted, check if they're accepted.
        participant = MatchParticipant.objects.get(id=participant_id)

        # Check wherher they can be accepted.
        if participant.accepted:
            #return HttpResponse('Participant already accepted.')
            messages.warning(request, "Participant already accepted")
            return redirect(reverse('kitup:web_response'))
        elif not participant.match.owner is request.user:
            #return HttpResponse('You do not have permission to accept the user')
            messages.error(request, "You do not have permission to accept the user")
            return redirect(reverse('kitup:web_response'))
        elif match.is_in_past():
            #return HttpResponse('Match is in past, cannot accept additional players.')
            messages.error(request, "Match is in past, cannot accept additional players")
            return redirect(reverse('kitup:web_response'))
        elif match.sport.max_participants <= MatchParticipant.objects.filter(match=participant.match, accepted=True):
            #return HttpResponse('The maximum number of participants have been accepted.')
            messages.error(request, "The maximum number of participants have been accepted")
            return redirect(reverse('kitup:web_response'))

        # Finally, update the status of the participant.
        participant.accepted = True
        participant.save()

    except MatchParticipant.DoesNotExist:
        #return HttpResponse('Match participant does not exist.')
        messages.error(request, "Match participant does not exist")
        return redirect(reverse('kitup:web_response'))

    # We have successfully accepted the participant.
    #return HttpResponse('Participant successfully accepted')
    messages.success(request, "Participant successfully accepted")
    return redirect(reverse('kitup:web_response'))

# Permits the owner to kick a player from the match.
@login_required
def match_kick(request, participant_id):
    
    try:

        # Get the participant that is being kicked.
        participant = MatchParticipant.objects.get(id=participant_id)

        # Check that the participant can be kicked.
        if match.is_in_past():
            #return HttpResponse('Cannot kick participant, match in the past')
            messages.error(request, "Cannot kick participant, match in the past")
            return redirect(reverse('kitup:web_response'))
        elif participant.match.owner is not request.user:
            #return HttpResponse('You do not have permission to kick yourself')
            messages.error(request, "You do not have permission to kick yourself")
            return redirect(reverse('kitup:web_response'))
        elif not participant.accepted:
            #return HttpResponse('The participant has not been accepted')
            messages.error(request, "The participant has not been accepted")
            return redirect(reverse('kitup:web_response'))

        # Finally, we can kick the participant from the match.
        participant.delete()

    except MatchParticipant.DoesNotExist:
        #return HttpResponse('The match participant does not exist.')
        messages.error(request, "The match participant does not exist")
        return redirect(reverse('kitup:web_response'))

    # We have successfully kicked the participant.
    #return HttpResponse('Participant successfully kicked')
    messages.success(request, "Participant successfully kicked")
    return redirect(reverse('kitup:web_response'))


# Permits the match to be viewed.
def match_view(request, match_id):

    context_dictionary = {}

    try:

        # Get the match and all the accepted participants.
        match = Match.objects.get(id=match_id)
        accepted_participants = MatchParticipant.objects.filter(match=match, accepted=True)

        print(f'{match.name}')

        profile = None
        participant = None
        is_owner = False
        pending_participants = None

        # If the user can be authenticated, update fields accordingly.
        if request.user.is_authenticated:

            print(f'{request.user.username}')

            # Update the context variables.
            profile = Profile.objects.get(user=request.user)
            if MatchParticipant.objects.filter(profile=profile, match=match).exists():
                participant = MatchParticipant.objects.get(profile=profile, match=match)
            is_owner = participant is not None and participant.match == match and match.owner == request.user
            if is_owner:
                pending_participants = MatchParticipant.objects.filter(match=match, accepted=False)

        # Set the match context values.
        context_dictionary['settings'] = settings
        context_dictionary['match'] = match
        context_dictionary['match_is_in_past'] = match.is_in_past()
        context_dictionary['match_is_full'] = match.sport.max_participants <= accepted_participants.count()
        context_dictionary['match_accepted_participants'] = accepted_participants
        context_dictionary['match_pending_participants'] = pending_participants

        # Set the user context values.
        context_dictionary['user_is_owner'] = is_owner
        context_dictionary['user_participant'] = participant

        # Add any of the page forms.
        context_dictionary['report_participant_form'] = MatchParticipantReportForm()

        print(context_dictionary)

    except Match.DoesNotExist:
        #return HttpResponse('Match does not exist.')
        messages.error(request, "Match does not exist")
        return redirect(reverse('kitup:web_response'))

    # Finally, render the view.
    return render(request, 'kitup/match_view.html', context_dictionary)

# Post view enables players to be ranked.
@login_required
def match_rate(request, participant_id):
    pass
