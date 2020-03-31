from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User

#  The models and forms for the kitup app.
from kitup.forms import UserForm, ProfileForm, UserLoginForm, MatchForm, UserUpdateForm, EmailPasswordRecovery, MatchParticipantReportForm
from kitup.models import Profile, Sport, Match, MatchParticipant, MatchParticipantReport

# The main index / home page for the website.
def index(request):
    context_dictionary = {}
    response = render(request, 'kitup/index.html', context_dictionary)
    return response


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

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
            return HttpResponse("Registration Failed") # For debugging purposes

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    # Render the template using the forms.
    response = render(request, 'kitup/user_register.html',
                      {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
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
                    return HttpResponse('Your KitUp account has been disabled.')
            else:
                print(f'Invalid login details: {username} {password}')
                return HttpResponse('Invalid details supplied.')

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
@login_required(login_url='kitup:user_login')
def user_profile(request):
    context_dictionary = {}
    context_dictionary['user_update_form'] = UserUpdateForm

    user_meta_data = User.objects.get(username=request.user)

    context_dictionary['first_name'] = user_meta_data.first_name
    context_dictionary['last_name'] = user_meta_data.last_name
    context_dictionary['email'] = user_meta_data.email

    #print(user_meta_data.Profile.strikes)
    response = render(request, 'kitup/user_profile.html', context_dictionary)
    return response


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
    match_create_form = MatchForm()
    cd = {'match_creation_form': match_create_form}
    response = render(request, 'kitup/match_create.html', cd)
    return response

# The user attempts to join the match.
@login_required
def match_join(request, match_id):

    try:

        # The profile of the joining user and the match they're attempting to join.
        profile = Profile.objects.get(user=request.user)
        match = Match.objects.get(id=match_id)

        # Check that the match can be joined
        if match.is_in_past():
            return HttpResponse('Match in the past, cannot join')

        # Handle if they've already joined the match.
        participant = None
        if MatchParticipant.objects.filter(profile=profile).exists():

            # Check their request.
            participant = MatchParticipant.objects.get(profile=profile)
            if participant.accepted:
                return HttpResponse('Already accepted')
            else:
                return HttpResponse('Awaiting Response')

        # Determine if the user can directly join.
        accepted = True
        if match.private or match.sport.max_participants <= MatchParticipant.objects.filter(match=match, accepted=True).count():
            accepted = False

        # Finally, create the instance of participant.
        participant = MatchParticipant(profile=profile, match=match, accepted=accepted)
        participant.save()

    except Match.DoesNotExist:
        return HttpResponse('Match does not exist.')

    # An Should not reach this point.
    return HttpResponse('Participation request made.')

# The user is attempting to leave the match.
@login_required
def match_leave(request, match_id):

    try:

        # The match being left and the leaving profile.
        profile = Profile.objects.get(user=request.user)
        match = Match.objects.get(id=match_id)

        # If the match is in the past, prevent them from leaving.
        if match.is_in_past():
            return HttpResponse('Failed to leave, match in the past.')

        # The match owner has deleted their match, return to index.
        if match.owner is request.user:
            match.delete()
            return redirect(reverse('kitup:index'))

        # If the player is a participant, delete their participation instance.
        if not MatchParticipant.objects.filter(profile=profile,match=match).exists():
            return HttpResponse('You are not a participant')
        participant = MatchParticipant(profile=profile,match=match)
        participant.delete()

    except Match.DoesNotExist:
        return HttpResponse('Match does not exist.')

    # Redirect them back to the match view page.
    return redirect(reverse('kitup:match_view', kwargs={'match_id': match.id}))

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

# Permits the match to be viewed.
def match_view(request, match_id):

    context_dictionary = {}

    try:

        # Get the match being viewed, and the profile viewing the match.
        profile = Profile.objects.get(user=request.user)
        match = Match.objects.get(id=match_id)

        # Gets all of the participants.
        accepted_participants = MatchParticipant.objects.filter(match=match, accepted=True)

        # Check if the user is participating.
        participant = None
        if not MatchParticipant.objects.filter(profile=profile, match=match).exists():
            participant = MatchParticipant.objects.get(profile=profile, match=match)

        # If the user is an owner, get the pending requests.
        is_owner = participant is not None and participant.match is match and match.owner is request.user
        pending_participants = None
        if is_owner:
            pending_participants = MatchParticipant.objects.filter(match=match, accepted=False)

        # Set the match context values.
        context_dictionary['match'] = match
        context_dictionary['match_is_in_past'] = match.is_in_past()
        context_dictionary['match_is_full'] = match.sport.max_participants <= participant.count()
        context_dictionary['match_accepted_participants'] = accepted_participant
        context_dictionary['match_pending_participants'] = pending_participants

        # Set the user context values.
        context_dictionary['user_is_owner'] = participant is not None and participant.match is match and match.owner is request.user
        context_dictionary['user_is_participating'] = participant is not None
        context_dictionary['user_participant'] = participant

    except Match.DoesNotExist:
        return HttpResponse('Match does not exist.')

    # Finally, render the view.
    return render(request, 'kitup/match_view.html', context_dictionary)

# Post view enables players to be ranked.
@login_required
def match_rate(request, match_id):

    pass
