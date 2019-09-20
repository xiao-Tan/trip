from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime
from dateutil import parser

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password_confirm'] != postData['password']:
            errors["password_confirm"] = "Passwords should match"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if check_if_email_exist(postData['email']) == True:
            errors['email'] = "Registered email should be unique"
        if postData['birthday'] == '':
            errors["birthday"] = "Birthday should not be empty"
        else: 
            if parser.parse(postData["birthday"]).date() >= datetime.date.today():
                errors["birthday"] = "Birthday should be in the past" 
            else:
                if (datetime.date.today() - parser.parse(postData["birthday"]).date()).days < (13 * 365):
                    errors["birthday"] = "COPPA compliant!"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email_address=postData['login_email'])
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['login_password'].encode(), logged_user.password.encode()):
                errors['login_password'] = "Please try again!"
        else:
            errors['login_email'] = "Please try again!"
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors["destination"] = "Destination should be at least 3 characters"
        if len(postData['plan']) < 3:
            errors["plan"] = "Plan should be at least 3 characters"
        if postData['start_date'] == '':
            errors["start_date"] = "Start_date should not be empty"
        else:
            if parser.parse(postData["start_date"]).date() <= datetime.date.today():
                errors["start_date"] = "Start_date should be in the future" 
        if postData['end_date'] == '':
            errors["end_date"] = "End_date should not be empty"
        else:
            if parser.parse(postData["end_date"]).date() <= parser.parse(postData["start_date"]).date():
                errors["end_date"] = "End_date should after the start date"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    birthday = models.DateField(blank=True,null=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
    #trips_join
    #trips


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.TextField()
    users_join = models.ManyToManyField(User, related_name = "trips_join")
    users_created = models.ForeignKey(User, related_name = "trips")
    objects = TripManager()


def check_if_email_exist(email_address):
    all_users = User.objects.all()
    for v in all_users:
        if email_address == v.email_address:
            return True
    return False