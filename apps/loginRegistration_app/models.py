from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime

class RegistrationManager(models.Manager):
    def Register(self, postData):
        error_list = []
        now = datetime.now()
        # First name valication
        if len(postData['fname']) < 1:
            error_list.append ('First name cannont be empty')

        #Last name validation
        if len(postData['lname']) < 1:
            error_list.append('Last name cannont be empty')

        #Email validation
        if len(postData['email']) < 1:
            error_list.append('Email cannont be empty')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if EMAIL_REGEX.match(postData['email']):
            if self.filter(email = postData['email']):
                error_list.append('Email already exists')
        else:
            error_list.append('Invalid email format')

        #Birthday validation
        if len(postData['bday']) < 1:
            error_list.append('Enter date of birth')
        else:
            if datetime.strptime(postData['bday'], '%Y-%m-%d') > now:
                error_list.append('Date of birth cannot be before today')

        #Password validation
        if len(postData['pword']) < 8:
            error_list.append('Password must at least be 8 characters long')

        if not postData['pword'] == postData['c_pword']:
            error_list.append('Password does not match')

        if len(error_list) < 1:
            en_pword = postData['pword'].encode()
            hashed_pw = bcrypt.hashpw(en_pword, bcrypt.gensalt())
            self.create(first_name = postData['fname'], last_name = postData['lname'], email = postData['email'], birthday = postData['bday'], password = hashed_pw)
            userData = self.filter(email =postData['email'])
            context = {'status': 1, 'response': userData[0]}
            return context
        else:
            context={'status': 0,'response': error_list}
            return context

    def login(self, postData):
        login_error = []
        if len(postData['email']) < 1 or len(postData['pword']) < 1:
            login_error.append('Please enter Email and password')
            context = {'status':0, 'response':login_error}
            return context
        else:
            userData = self.filter(email = postData['email'])
            if not userData:
                login_error.append('Email does not exists')
                context = {'status': 0, 'response': login_error}
                return context
            else:
                if bcrypt.hashpw(postData['pword'].encode(), userData[0].password.encode()) == userData[0].password:
                    context = {'status': 1, 'response': userData[0]}
                    return context
                else:
                    login_error.append('The password is incorrect')
                    context ={'status': 0, 'response': login_error}
                    return context


class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()
    birthday = models.DateTimeField()
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = RegistrationManager()
# Create your models here.
