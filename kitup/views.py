from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# The main page for the website.
def index(request):
	context_dictionary = {}
	response = render(request, 'kitup/index.html', context_dictionary)
	return response


# Invoked to display the registration view to the new user.
def user_register(request):
	context_dictionary = {}
	response = render(request, 'kitup/register.html', context_dictionary)
	return response


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