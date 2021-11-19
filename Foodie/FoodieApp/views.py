from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'reg_log.html')


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
            'this_user': this_user
        }
        return render(request, 'dashboard.html', context)

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

def logout(request):
    del request.session['user_id']
    return redirect('/')