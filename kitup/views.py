from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User

# The main page for the website.
from kitup.forms import UserForm, ProfileForm, UserLoginForm, MatchForm, UserUpdateForm, EmailPasswordRecovery

from kitup.models import Profile

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

            # Check whether or not the user uploaded a picute.
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # Finally, save the profile and denote registered as True.
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
# @login_required(login_url='kitup:login')
def user_profile(request):
    context_dictionary = {}
    context_dictionary['user_update_form'] = UserUpdateForm

    response = render(request, 'kitup/user_profile.html', context_dictionary)
    return response


# Permits the viewing of another players profile.
def user_view_profile(request, user_id):
    pass


# Permits the user to edit / alter their settings.
@login_required
def user_settings(request):
    pass


# Permits the user to report another user.
@login_required
def user_report(request, reported_user_id):
    pass


# The match creation form.
@login_required
def match_create(request):
    match_create_form = MatchForm()
    cd = {'match_creation_form': match_create_form}
    response = render(request, 'kitup/match_create.html', cd)
    return response


# Enables the user to leave a match they're in.
@login_required
def match_leave(request, match_id):
    pass


# Accessed post match to rate the players within the game.
def match_view(request, match_id):
    response = render(request, 'kitup/match_view.html')
    return response


# Post view enables players to be ranked.
@login_required
def match_rate(request, match_id):
    pass


# Enables players to join teams for a given match
@login_required
def match_join(request, match_id):
    pass
