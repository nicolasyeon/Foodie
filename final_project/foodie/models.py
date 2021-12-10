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

class Collage(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(
        User, related_name="created_collage", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Restaurants(models.Model):
    restaurant_id = models.CharField(max_length=255)
    collages = models.ManyToManyField(Collage, related_name="restaurants")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)