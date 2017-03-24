from __future__ import unicode_literals

from django.db import models

import bcrypt, datetime


# Create your models here.
class UserManager(models.Manager):
    def add_user(self, postData):
        errors = []
        if len(postData["name"]) < 3:
            errors.append("Name must be at least 3 characters")
        if len(postData["username"]) < 3:
            errors.append("Username must be at least 3 characters")
        if len(postData["password"]) < 8:
            errors.append("Password must be at least 8 characters")
        if postData["password"] != postData["confirm_password"]:
            errors.append("Password and Confirm Password must match")
        if self.filter(username = postData["username"]):
            errors.append("This username has already been registered.")

        try:
            date_hired = datetime.datetime.strptime(postData["date_hired"], "%m/%d/%Y")
            if date_hired > datetime.datetime.now():
                errors.append("Date hired cannot be in the future.")
        except ValueError:
            errors.append("Please enter date hired in mm/dd/yyyy format.")

        if not errors:
            pw_hash = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            user = self.create(name=postData["name"], username=postData["username"], date_hired=date_hired, pw_hash = pw_hash)
            return (True, user)
        else:
            return (False, errors)

    def login(self, postData):
        try:
            user = Users.objects.get(username = postData["username"])
            if not bcrypt.checkpw(postData["password"].encode(), user.pw_hash.encode()):
                return (False, "Password incorrect")
        except:
            return (False, "Username is not registered")

        user = Users.objects.get(username=postData["username"])
        return (True, user)


class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
