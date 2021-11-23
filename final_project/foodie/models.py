from django.db import models
from datetime import datetime, date
import re
import bcrypt


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email_checker = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['pw']) < 8:
            errors['pw'] = "Your password must be at least 8 characters"
        if len(postData['fname']) < 2 or len(postData['lname']) < 2:
            errors['name'] = "Your name must be at least 2 characters"
        if not email_checker.match(postData['email']):
            errors['email'] = "Email must be valid"
        if postData['pw'] != postData['confpw']:
            errors['pw'] = "Password and Confirm Password do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['login_pw'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()

class ReviewManager(models.Manager):
    def add_review_validator(self, postData):
        errors = {}
        if len(postData['restaurant_name']) < 3:
            errors['restaurant_name'] = "A restaurant's name should be at least 3 characters!"
        if len(postData['location']) < 1:
            errors['location'] = "A location must be provided!"
        if len(postData['content']) < 1:
            errors['content'] = "Content must be provided!"
        return errors

class Review(models.Model):
    restaurant_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    rating = models.IntegerField()
    content = models.CharField(max_length=255)
    creator = models.ForeignKey(
        User, related_name="has_created_review", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_reviews")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = ReviewManager()