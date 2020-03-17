from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

# The main page for the website.
from kitup.forms import UserForm


def index(request):
    context_dictionary = {}
    response = render(request, 'kitup/index.html', context_dictionary)
    return response


'''
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from kitup.forms import UserRegistrationForm


# The main page for the website.
def index(request):
    # Create the context dictionary; contains the available games.
    context_dictionary = {}

    # Render the index response i.e. create the template.
    response = render(request, 'kitup/index.html', context_dictionary)
    return response

'''


# Invoked to display the registration view to the new user.
def user_register(request):
    registered = False

    if request.method == 'POST':
        user_reg = UserForm(request.POST)

        # If the two forms are valid...
        if user_reg.is_valid():
            # Save the user's form data to the database.
            user = user_reg.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            # Uses form validation to check that the set password matches
            user.set_password(user.password) # Need to update later with the Forms API
            user.save()
            registered = True
        else:
            # Print problems to the terminal.
            print(user_reg.errors)

    else:
        user_reg = UserForm()

    # Render the template depending on the context.
    return render(request,
                  'kitup/register.html',
                  context={'user_reg': user_reg,
                           'registered': registered})


# Invoked in the event the user wants to log into their account.
def user_login(request):
    # Create the context dictionary for the login request.
    context_dictionary = {}

    # Render the login response i.e. create the template.
    response = render(request, 'kitup/login.html', context_dictionary)
    return response


# Invoked in the event the user wishes to log out.
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('kitup:index'))


# Invoked in the event the user wants to log into their account.
def user_login(request):
    context_dictionary = {}
    response = render(request, 'kitup/login.html', context_dictionary)
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
    pass


# Permits the viewing of another players profile.
def view_profile(request, user_id):
    pass


# Permits the user to edit / alter their settings.
@login_required
def user_settings(request):
    pass


# Permits the user to report another user.
@login_required
def user_report(request, reported_user_id):
    pass


# Permits the creation of a match.
@login_required
def match_create(request):
    pass


# Enables the user to leave a match they're in.
@login_required
def match_leave(request, match_id):
    pass


# Find a match based on the name.
def match_find(request, match_name):
    pass


# View a given match based on the match id.
def match_view(request, match_id):
    pass


# Post view enables players to be ranked.
@login_required
def match_post(request, match_id):
    pass


# Enables players to join teams for a given match
@login_required
def match_join(request, match_id):
    pass
