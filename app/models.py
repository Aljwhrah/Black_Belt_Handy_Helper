from datetime import datetime, timedelta

import bcrypt
import re
from django.db import models

class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            errors['email'] = 'There was a problem'

        elif not bcrypt.checkpw(
            post_data['password'].encode(),
            user_list[0].password.encode()

        ):
            errors['password'] = 'There was a problem'
        return errors

    def register_validator(self, post_data):
        errors = {}
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex,post_data['email'])):
            pass
        else:
            errors['email'] = 'email must be longer than 8 characters'

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be longer than 8 characters'
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be longer than 8 characters'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be longer than 2 characters'

        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Password does not match'

        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = 'The email is already registered'

        return errors

class JobManager(models.Manager):
    def job_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 3:
            errors['title'] = "item must be longer than 3 characters."
        if len(post_data['description']) < 3:
            errors['description'] = "description must be longer than 3 characters."
        if len(post_data['location']) < 3:
            errors['location'] = "location must be longer than 3 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    # liked_books
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name='jobs_uploaded', on_delete=models.CASCADE)
    users_who_add = models.ManyToManyField(User, related_name='adedd_jobs')
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    on_add = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()