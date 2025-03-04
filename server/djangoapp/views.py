from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, DealerReview

# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, submit_review
import requests
# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
# default view

def home(request):
    url = "http://localhost:3000/dealerships/get"
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url)
    # Concat all dealer's short name
    #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    context = {
        'username': "none",
        'status': "logged out",
        'dealership_list': dealerships
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
        context["username"] = "none"
        return render(request, 'djangoapp/index.html', context)
        # Return an 'invalid login' error message.
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {
        'username': "NONE",
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
    url = "http://localhost:3000/dealerships/get"
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url)
    # Concat all dealer's short name
    #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    context = {
        'username': username,
        'status' : "logged in",
        'dealership_list': dealerships
    }
    
    user = User.objects.create_user(username = username, email = '', password = password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    context["status"] = "logged in"
    return render(request, 'djangoapp/index.html', context)
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, username, status):
    url = "http://localhost:3000/dealerships/get"
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url)
    # Concat all dealer's short name
    #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
    context = {
        'username': username,
        'status' : status,
        'dealership_list': dealerships
    }
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# # Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, username, status, dealer_id):
    context = {
        'username': username,
        'status' : status,
        'dealer_id': dealer_id,
        'reviews': []
    }
    url = "http://localhost:5000/api/get_reviews"
    # Get dealers from the URL
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    context['reviews'] = reviews
    if request.method == "GET":
        return render(request, 'djangoapp/dealer_details.html', context)

# # Create a `add_review` view to submit a review
def add_review(request, username, status, dealer_id):
    print("add review", username, status, dealer_id)
    url = "http://localhost:3000/dealerships/get"
    dealership = get_dealer_by_id_from_cf(url, dealer_id)

    context = {
        'username': username,
        'status' : status,
        'dealer_id': dealer_id,
        'dealership': dealership,
    }
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)


def post_review(request, username, status, dealer_id):
    [review, purchase, purchase_date] = [request.POST['review-input'], request.POST['purchase-input'], request.POST['purchase-date-input']]
    [car_make, car_model, car_year] = [request.POST['car-make-input'], request.POST['car-model-input'], request.POST['car-year-input']]
    url = "http://localhost:3000/dealerships/get"
    dealership = get_dealer_by_id_from_cf(url, dealer_id)
    json_data = {   'id' : dealer_id, 
                    'name' : username, 
                    'dealership' : dealer_id, 
                    'review' : review, 
                    'purchase' : purchase, 
                    'purchase_date' : purchase_date,
                    'car_make' : car_make, 
                    'car_model' : car_model,
                    'car_year' : car_year,
                }
    url = "http://localhost:5000/api/post_review"
    context = {
        'username': username,
        'status' : status,
        'dealer_id': dealer_id,
        'reviews': []
    }
    url = "http://localhost:5000/api/get_reviews"
    # Get dealers from the URL
    reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
    context['reviews'] = reviews
    if request.method == "POST":
        return render(request, 'djangoapp/dealer_details.html', context)