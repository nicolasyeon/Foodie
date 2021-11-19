from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import requests
import json
import geocoder

def index(request):
    return render(request, 'index.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
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
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        return redirect('/dashboard')

def dashboard(request):
    this_user = User.objects.get(id=request.session['user_id'])
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'liked_reviews': Review.objects.filter(liked_by=this_user),
            'all_reviews': Review.objects.all(),
            'this_user': this_user,
        }
        return render(request, 'index.html', context)

def new_review(request, user_id):
    return render(request, 'create_review.html')

def create_review(request, user_id):
    errors = Review.objects.add_review_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/new_review/{user_id}')
    else:
        user = User.objects.get(id=request.session['user_id'])
        review = Review.objects.create(
            restaurant_name=request.POST['restaurant_name'],
            location=request.POST['location'],
            content=request.POST['content'],
            rating=request.POST['rating'],
            creator=user
        )
        return redirect('/dashboard')

def remove_review(request, review_id):
    review = Review.objects.get(id=review_id)
    review.delete()

    return redirect('/dashboard')

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

def view_review(request, review_id):
    context = {
        'review': Review.objects.get(id=review_id),
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'view_review.html', context)

def edit_review(request, review_id):
    errors = Review.objects.add_review_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/view_review/{review_id}')
    else:
        to_update = Review.objects.get(id=review_id)
        to_update.restaurant_name = request.POST['restaurant_name']
        to_update.location = request.POST['location']
        to_update.rating = request.POST['rating']
        to_update.content = request.POST['content']        
        to_update.save()
    return redirect('/dashboard')

def like(request, review_id):
    if request.method == "GET":
        review = Review.objects.get(id=review_id)
        user = User.objects.get(id=request.session['user_id'])
        review.liked_by.add(user)
        review.save()
    return redirect('/dashboard')

def unlike(request, review_id):
    if request.method == "GET":
        review = Review.objects.get(id=review_id)
        user = User.objects.get(id=request.session['user_id'])
        review.liked_by.remove(user)
        review.save()
    return redirect('/dashboard')

def list_restaurants(request):
    api_key='aLUc-OJHBOGh-udAIY-aPFp-D2tSpgak6LezeQAr2pqYmg9YvHbHUoA-OkgT0tY5oagf-dxmbj7XpNZsEV-viFFgaP0TSvZEzWRJB4veY0_6-qpkRF1IEZxplvR0YXYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    
    if request.method == "POST":
        # restaurant_name = request.POST['restaurant_name']
        # location = request.POST['location']
        # element = request.POST['distance' or 'review_count']
        # params = { 'term': restaurant_name, 'location': location, 'sort_by': element }

        # restaurant_name = request.POST['restaurant_name']
        # location = request.POST['location']
        # distance = request.POST['distance']
        # params = { 'term': restaurant_name, 'location': location, 'sort_by': distance }
        
        # restaurant_name = request.POST['restaurant_name']
        # location = request.POST['location']
        # review_count = request.POST['review_count']
        # params = { 'term': restaurant_name, 'location': location, 'sort_by': review_count }

        restaurant_name = request.POST['restaurant_name']
        location = request.POST['location']
        review_count = request.POST.get('review_count')
        distance = request.POST.get('distance')
        if distance == None:
            params = { 'term': restaurant_name, 'location': location, 'sort_by': review_count }
        else:
            params = { 'term': restaurant_name, 'location': location, 'sort_by': distance }
        req = requests.get(url, params=params, headers=headers)
        parsed = json.loads(req.text)
        print(params)
        # print(parsed)

        businesses = parsed["businesses"]
        
        for business in businesses:
            business['display_address'] = " ".join(business["location"]["display_address"])
            business['distance'] = distance
            distance = round(distance)

        context = {
            'businesses': businesses,
            'params': params,
        }
        return render(request, 'list_of_restaurants.html', context)
    else:
        return render(request, 'list_of_restaurants.html', {})

def current_location(request):
    if request.method == "POST":
        g = geocoder.ip('me')
        current_location = g.address
        context = {
            'current_location': current_location
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'list_of_restaurants.html', {})

def logout(request):
    del request.session['user_id']
    return redirect('/')