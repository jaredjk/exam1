from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1 or len(postData['username']) < 1 or len(postData['password']) < 1 or len(postData['confirm_password']) < 1:
            errors["all"] = "Fields cannot be empty"
            return errors
        if len(postData['name']) < 4:
            errors["name"] = "Name has to be at least 3 Character"
        if len(postData['username']) < 4:
            errors["username"] = "Username shas to be at least 3 Character"
        if len(postData['password']) < 8:
            errors["password_length"] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Password does not match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}>".format(self.name)

class Quote(models.Model):
    quotename = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name="quotes_added")
    quoted_by = models.ManyToManyField(User, related_name="quotes_quoted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "<Book object: {}>".format(self.quotename)