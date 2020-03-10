from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# The main page for the website.
def index(request):

	# Create the context dictionary; contains the available games.
	context_dictionary = {}

	# Render the index response i.e. create the template.
	response = render(request, 'kitup/index.html', context_dictionary)
	return response

# Invoked to display the registration view to the new user.
def user_register(request):
	
	# Create a context dictionary for the response.
	context_dictionary = {}

	# Render the register response i.e. create the template.
	response = render(request, 'kitup/register.html', context_dictionary)
	return response

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