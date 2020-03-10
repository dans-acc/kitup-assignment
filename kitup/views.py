from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# The main index page for the site.
def index(request):
	pass

# The page used to register a new account.
def register(request):
	pass

# The page used to login.
def login(request):
	pass

# The page used to logout.
def logout(request):
	pass
