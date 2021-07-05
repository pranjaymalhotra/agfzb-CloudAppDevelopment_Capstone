from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, store_review
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def get_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context["message"] = "Invalid username or password"
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def get_logout(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/logout.html', context)

def signup_view( request ):
    context = {
        'err': ''
    }
    return render( request, 'djangoapp/registration.html', context ) 
def registration_request(request):
    if request.method == 'POST':
        user_exist = False
        username = request.POST[ 'username' ]
        email = request.POST[ 'email' ]
        f_name = request.POST[ 'f_name' ]
        l_name = request.POST[ 'l_name' ]
        psw = request.POST[ 'psw' ]
        psw2 = request.POST[ 'psw2' ]
        if psw != psw2:
            return render( request, 'djangoapp/registration.html', {
                'err': 'Error! Passwords do not match... {0}, {1}'.format( psw, psw2 )
            } )  
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} New user".format(username))
        if not user_exist:
            user = User.objects.create_user( username, email, psw, first_name=f_name, last_name=l_name )
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', 
            {
                'err': 'You are already Registered'
            })

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://4c16990c.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url)
        context['reviews'] = filter(lambda x: x.dealership == dealer_id, reviews)
        context['dealer_id'] = dealer_id
        context['dealer'] = get_dealer_detail_infos(dealer_id)
    return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    if request.method == "GET":
        context = {}
        context['dealer_id'] = dealer_id
        context['dealer'] = get_dealer_detail_infos(dealer_id)
        context['cars'] = CarModel.objects.all()
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        url = "https://4c16990c.us-south.apigw.appdomain.cloud/api/review"
        payload = {}
        payload['name'] = request.POST['username']
        payload['dealership'] = dealer_id
        payload['review'] = request.POST['review']
        payload['purchase'] = request.POST['purchase']
        payload['purchase_date'] = request.POST['purchase_date']
        car = CarModel.objects.get(id = request.POST['car'])
        if car:
            payload['car_make'] = car.make.name
            payload['car_model'] = car.name
            payload['car_year'] = car.year.strftime("%Y")
        store_review(url, payload)
    return redirect('djangoapp:dealer_details', dealer_id = dealer_id)

def get_dealer_detail_infos(dealer_id):
    url = "https://4c16990c.us-south.apigw.appdomain.cloud/api/dealership"
    dealerships = get_dealers_from_cf(url)
    return next(filter(lambda x: x.id == dealer_id, dealerships))
