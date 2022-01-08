from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
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

def collection_page(request):
    context = {
            'all_collections': Collection.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
    return render(request, 'collection.html', context)

def discover_collection_page(request):
    context = {
            'all_collections': Collection.objects.all(),
        }
    return render(request, 'discover.html', context)

def create_collection_page(request, user_id):
    return render(request, 'create_collection.html')

def create_collection(request, user_id):
    user = User.objects.get(id=request.session['user_id'])
    collection = Collection.objects.create(
        name=request.POST['name'],
        description=request.POST['description'],
        photo=None
    )
    collection.creators.add(user)
    return redirect('/collection_page')

def edit_collection(request,collection_id):
    to_edit = Collection.objects.get(id=collection_id)
    to_edit.name = request.POST['name']
    to_edit.description = request.POST['description']
    to_edit.save()
    return redirect(f'/collection_detail/{collection_id}')

def edit_collection_page(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    Restaurants = collection.restaurants.all()
    creators = collection.creators.all()
    if Restaurants in collection.restaurants.all() == 0:
        return render(request, 'collection_detail.html', {})
    else:
        api_key = os.getenv("API_KEY")
        headers = {'Authorization': 'Bearer %s' % api_key}
        businesses = []
        for Restaurants in collection.restaurants.all():
            url = 'https://api.yelp.com/v3/businesses/{}'.format(Restaurants.restaurant_id)
            req = requests.get(url, headers=headers)
            parsed = json.loads(req.text)
            businesses.append(parsed)
        
        context = {
            'restaurant': Restaurants,
            'creators': creators,
            'collection': Collection.objects.get(id=collection_id),
            'businesses': businesses,
            'all_collections': Collection.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id']),
            'all_users': User.objects.all()
        }
        return render(request, 'edit_collection.html', context)


def add_to_collection(request, business_id):
    if request.method == "POST":
        restaurants = Restaurants.objects.create(
            restaurant_id=request.POST['restaurant_id'],
        )
        context = {
            'restaurant' : restaurants,
            'all_restaurants' : Restaurants.objects.all(),
            'all_collections': Collection.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'collection.html', context)

def add_restaurant(request, collection_id, restaurant_id):
    collection = Collection.objects.get(id=collection_id)
    restaurants = Restaurants.objects.get(id=restaurant_id)
    restaurants.collections.add(collection)
    return redirect('/collection_page')

def add_photo(request, collection_id):
    add_image = Collection.objects.get(id=collection_id)
    add_image.photo=request.POST['image']
    add_image.save()
    return redirect('/collection_page')

def collection_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    Restaurants = collection.restaurants.all()
    creators = collection.creators.all()
    if Restaurants in collection.restaurants.all() == 0:
        return render(request, 'collection_detail.html', {})
    else:
        api_key = os.getenv("API_KEY")
        headers = {'Authorization': 'Bearer %s' % api_key}
        businesses = []
        for Restaurants in collection.restaurants.all():
            url = 'https://api.yelp.com/v3/businesses/{}'.format(Restaurants.restaurant_id)
            req = requests.get(url, headers=headers)
            parsed = json.loads(req.text)
            businesses.append(parsed)
        
        context = {
            'restaurant': Restaurants,
            'creators': creators,
            'collection': Collection.objects.get(id=collection_id),
            'businesses': businesses,
            'all_collections': Collection.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'collection_detail.html', context)

def discover_collection_detail(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    Restaurants = collection.restaurants.all()
    creators = collection.creators.all()
    if Restaurants in collection.restaurants.all() == 0:
        return render(request, 'collection_detail.html', {})
    else:
        api_key = os.getenv("API_KEY")
        headers = {'Authorization': 'Bearer %s' % api_key}
        businesses = []
        for Restaurants in collection.restaurants.all():
            url = 'https://api.yelp.com/v3/businesses/{}'.format(Restaurants.restaurant_id)
            req = requests.get(url, headers=headers)
            parsed = json.loads(req.text)
            businesses.append(parsed)
        
        context = {
            'restaurant': Restaurants,
            'creators': creators,
            'collection': Collection.objects.get(id=collection_id),
            'businesses': businesses,
            'all_collections': Collection.objects.all(),
        }
        return render(request, 'collection_detail.html', context)

def remove_restaurant(request, collection_id, restaurant_id):
    restaurant = Restaurants.objects.get(id=restaurant_id)
    restaurant.delete()
    return redirect(f'/collection_detail/{collection_id}')

def remove_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection.delete()
    return redirect('/collection_page')

def add_user(request, collection_id, user_id):
    collection = Collection.objects.get(id=collection_id)
    user = User.objects.get(id=user_id)
    collection.creators.add(user)
    return redirect('/collection_page')

def remove_user(request, collection_id, user_id):
    collection = Collection.objects.get(id=collection_id)
    user = User.objects.get(id=user_id)
    collection.creators.remove(user)
    return redirect('/collection_page')

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

def like(request, collection_id):
    user = User.objects.get(id=request.session['user_id'])
    collection = Collection.objects.get(id=collection_id)
    user.likes.add(collection)
    return redirect ('/collection_page')

def dislike(request, collection_id):
    user = User.objects.get(id=request.session['user_id'])
    collection = Collection.objects.get(id=collection_id)
    user.likes.remove(collection)
    return redirect ('/collection_page')

def logout(request):
    del request.session['user_id']
    return redirect('/')