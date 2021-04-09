from django.db import models
import re

class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['user_name']) < 3:
            errors['user_name'] = "Name is too short"
        if len(reqPOST['alias']) < 2:
            errors['alias'] = "Alias is too short"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if reqPOST['password'] != reqPOST['password_conf']:
            errors['match'] = "Password and password conf dont match"
        if len(reqPOST['email']) < 6:
            errors['email'] = "Email is too short"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):            
            errors['regex'] = "Invalid email address"
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >= 1:
            errors['dup'] = "Email already in use"
        return errors

class User(models.Model):
    name = models.TextField()
    alias = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class IdeaManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['description']) < 10:
            errors['description'] = "Description is too short"
        idea_description = Idea.objects.filter(description=reqPOST['description'])
        if len(idea_description) >= 1:
            errors['dup'] = "Description already in use"
        return errors


class Idea(models.Model):
    description = models.TextField()
    creator = models.ForeignKey(User, related_name="ideas_created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = IdeaManager()

# Create your models here.
