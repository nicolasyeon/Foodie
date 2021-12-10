from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from dotenv import load_dotenv
import bcrypt
import requests
import json
import geocoder
import os

load_dotenv()

def index(request):
    return render(request, 'landing.html')

def register_page(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def collage_page(request):
    context = {
            'all_collages': Collage.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'collage.html', context)

def discover_collage_page(request):
    context = {
            'all_collages': Collage.objects.all(),
        }
    return render(request, 'discover.html', context)

def create_collage_page(request, user_id):
    return render(request, 'create_collage.html')

def create_collage(request, user_id):
    user = User.objects.get(id=request.session['user_id'])
    collage = Collage.objects.create(
        name=request.POST['name'],
        description=request.POST['description'],
        creator=user
    )
    return redirect('/collage_page')

def add_to_collage(request, business_id):
    if request.method == "POST":
        restaurants = Restaurants.objects.create(
            restaurant_id=request.POST['restaurant_id'],
        )
        context = {
            'restaurant' : restaurants,
            'all_restaurants' : Restaurants.objects.all(),
            'all_collages': Collage.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'collage.html', context)

def add_restaurant(request, collage_id, restaurant_id):
    collage = Collage.objects.get(id=collage_id)
    restaurants = Restaurants.objects.get(id=restaurant_id)
    restaurants.collages.add(collage)
    return redirect('/collage_page')

def collage_detail(request, collage_id):
    api_key = os.getenv("API_KEY")
    headers = {'Authorization': 'Bearer %s' % api_key}
    collage = Collage.objects.get(id=collage_id)
    businesses = []
    for restaurant in collage.restaurants.all():
        url = 'https://api.yelp.com/v3/businesses/{}'.format(restaurant.restaurant_id)
        req = requests.get(url, headers=headers)
        parsed = json.loads(req.text)
        businesses.append(parsed)

    context = {
        'restaurant': restaurant,
        'collage': Collage.objects.get(id=collage_id),
        'businesses': businesses,
        'all_restaurants' : Restaurants.objects.all(),
        'all_collages': Collage.objects.all(),
    }
    return render(request, 'collage_detail.html', context)

def remove_restaurant(request, collage_id, restaurant_id):
    restaurant = Restaurants.objects.get(id=restaurant_id)
    restaurant.delete()
    return redirect(f'/collage_detail/{collage_id}')

def remove_collage(request, collage_id):
    collage = Collage.objects.get(id=collage_id)
    collage.delete()
    return redirect('/collage_page')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_page')
    else:
        user = User.objects.create(
            first_name=request.POST['fname'],
            last_name=request.POST['lname'],
            email=request.POST['email'],
            password=bcrypt.hashpw(
                request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        print(user)
        return redirect('/dashboard')

def dashboard(request):
    this_user = User.objects.get(id=request.session['user_id'])
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'this_user': this_user,
        }
        return render(request, 'index.html', context)

# make a method where a user who has no account can explore
def explore(request):
    return render(request, 'index.html')

def view_account(request, user_id):
    one_user = User.objects.get(id=user_id)
    context = {
        'user': one_user
    }
    return render(request, 'view_account.html', context)

def edit_account(request, user_id):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/view_account/{user_id}')
    else:
        to_update = User.objects.get(id=user_id)
        to_update.first_name = request.POST['fname']
        to_update.last_name = request.POST['lname']
        to_update.save()
    return redirect(f'/view_account/{user_id}')

def list_restaurants(request):
    api_key = os.getenv("API_KEY")
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    
    if request.method == "POST":
        restaurant_name = request.POST['restaurant_name']
        location = request.POST['location']
        review_count = request.POST.get('review_count')
        distance = request.POST.get('distance')
        price1 = request.POST.get('1')
        price2 = request.POST.get('2')
        price3 = request.POST.get('3')
        price4 = request.POST.get('4')
        open_now = request.POST.get('open_now')
        params = { 'term': restaurant_name, 'location': location }
        if review_count in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'sort_by': review_count }
        if distance in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'sort_by': distance }
        if price1 in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'price': price1 }
        if price2 in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'price': price2 }
        if price3 in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'price': price3 }
        if price4 in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'price': price4 }
        if open_now in request.POST:
            params = { 'term': restaurant_name, 'location': location, 'open_now': True }
        req = requests.get(url, params=params, headers=headers)
        parsed = json.loads(req.text)

        businesses = parsed["businesses"]
        print(businesses)
        for business in businesses:
            business['display_address'] = " ".join(business["location"]["display_address"])
            meters = business['distance']
            miles = meters * 0.000621371
            miles = round(miles, 2)
            business['distance'] = miles

        context = {
            'businesses': businesses,
            'params': params,
        }
        return render(request, 'list_of_restaurants.html', context)
    else:
        return render(request, 'list_of_restaurants.html', {})

def select_category(request):
    api_key = os.getenv("API_KEY")
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    
    if request.method == "POST":
        g = geocoder.ip('me')
        current_location = g.address
        restaurant_name = request.POST.get('restaurant_name')
        hot_and_new = request.POST.get('hot_and_new')
        params = { 'term': restaurant_name, 'location': current_location }
        if hot_and_new in request.POST:
            params = { 'location': current_location, 'attributes': hot_and_new }
        req = requests.get(url, params=params, headers=headers)
        parsed = json.loads(req.text)

        businesses = parsed["businesses"]

        for business in businesses:
            business['display_address'] = " ".join(business["location"]["display_address"])
            meters = business['distance']
            miles = meters * 0.000621371
            miles = round(miles, 2)
            business['distance'] = miles

        context = {
            'businesses': businesses,
            'params': params,
        }
        return render(request, 'list_of_restaurants.html', context)
    else:
        return render(request, 'list_of_restaurants.html', {})

def current_location_index(request):
    if request.method == "POST":
        g = geocoder.ip('me')
        current_location = g.address
        context = {
            'current_location': current_location
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'list_of_restaurants.html', {})

def current_location_list_of_restaurants(request):
    if request.method == "POST":
        g = geocoder.ip('me')
        current_location = g.address
        context = {
            'current_location': current_location
        }
        return render(request, 'list_of_restaurants.html', context)
    else:
        return render(request, 'list_of_restaurants.html', {})

def logout(request):
    del request.session['user_id']
    return redirect('/')