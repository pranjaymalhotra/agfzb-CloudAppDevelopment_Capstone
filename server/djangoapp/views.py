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
    if request.method=='POST':
        user = request.POST[ 'username' ]
        password = request.POST[ 'psw' ]
        user = authenticate( username=user, password=password )
        if user is not None:
            login( request, user )
        return redirect( 'djangoapp:index' )
    return HttpResponseRedirect( reversed( 'index' ) )

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


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

