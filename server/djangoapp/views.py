from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# default view

def home(request):
    context = {
        'username': "none",
        'status': "logged out"
    }
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request, username, status):
    context = {
        'username': username,
        'status' : status
    }
    if request.method == "GET":
        return render(request, 'djangoapp/about_us.html', context)


# Create a `contact` view to return a static contact page
def contact(request, username, status):
    context = {
        'username': username,
        'status' : status
    }
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)

# Create a `login_request` view to handle sign in request
def login_view(request):
    username = request.POST['username-input']
    password = request.POST['password-input']
    context = {
        'username': username,
        'status' : ""
    }
    user = authenticate(request, username=username, password=password)
    if user is not None:
        context["status"] = "logged in"
        return render(request, 'djangoapp/index.html', context)
    else:
        context ["status"] = "Incorrect username or password"
        return render(request, 'djangoapp/index.html', context)
        # Return an 'invalid login' error message.
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {
        'username': NONE,
        'status' : "logged out"
    }
    if request.method == "GET":
        return render(request, "djangoapp/index.html", context)

# Create a `registration_request` view to handle sign up request
def registerpage(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)

def registration_request(request):
    username = request.POST['username-input']
    password = request.POST['password-input']
    first_name = request.POST['firstname-input']
    last_name = request.POST['lastname-input']
    context = {
        'username': username,
        'status' : "logged in"
    }
    user = User.objects.create_user(username, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    context["status"] = "logged in"
    return render(request, 'djangoapp/index.html', context)
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, username, status):
    context = {
        'username': username,
        'status' : status
    }
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# # Create a `get_dealer_details` view to render the reviews of a dealer
# # def get_dealer_details(request, dealer_id):
# # ...

# # Create a `add_review` view to submit a review
# # def add_review(request, dealer_id):
# # ...

