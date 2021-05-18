from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = 'First name must be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email format"
        existing_user = User.objects.filter(email = postData['email'])
        if len(existing_user) != 0:
            errors['email'] = "Email already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password and Confirm Password inputs must match"
        return errors

    def log_validator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Invalid email format"
        existing_user = User.objects.filter(email = postData['email'])
        if len(existing_user) != 1:
            errors['email'] = "User not found"
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['email'] = "Email and password do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)

    objects = UserManager()

class PostManager(models.Manager): # PostManager
    def post_validator(self, postData): # post_validator
        errors = {}
        if len(postData['title']) < 3: # code to match 'create' view
            errors['title'] = 'Title must be at least 5 characters'
        if len(postData['description']) < 25:
            errors['description'] = 'Post must have at least 25 characters'
        return errors

class Post(models.Model): # class Post, match below stuff to 'create' view
    user = models.ForeignKey(User, related_name='user_posts', on_delete = models.CASCADE)
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = PostManager()

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['comment']) < 1: # code to match 'comment' view
            errors['comment'] = 'Oops! Comment cannot be empty'
        return errors

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name='user_comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CommentManager()
# COULD ADD REPLIES! We could add a reply model here and replymanager. I am not 100% on the steps for this - save it for after class. 