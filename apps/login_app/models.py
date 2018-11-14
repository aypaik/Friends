from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# Create your models here.

class UserManager(models.Manager):
    def loginVal(self, postData):
        results = {'status': True, 'errors':[], 'user': None}
        users = self.filter(email = postData['email'])
        
        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results


    def creator(self, postData):
        user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
        return user
   
    # validate must take (self)
    def validate(self, postData):
        results = {'status': True, 'errors':[]}
        if len(postData['name']) < 3:
            results['errors'].append('Your name is too short.')
            results['status'] = False
        
        # check if first name is valid
        if not re.match("^[A-z][A-z|\.|\s]+$", postData['name']):
            results['errors'].append('Your name is not valid.')
            results['status'] = False
            
        if len(postData['alias']) < 3:
            results['errors'].append('Your alias is too short.')
            results['status'] = False

        if not re.match("^[A-z][A-z|\.|\s]+$", postData['alias']):
            results['errors'].append('Your alias is not valid.')
            results['status'] = False


        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid.')
            results['status'] = False

        if postData['password'] != postData['c_password']:
            results['errors'].append('Your passwords do not match.')
            results['status'] = False

        if len(postData['password']) < 8:
            results['errors'].append('Your password is too short.')
            results['status'] = False

        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append('User already exists.')
            results['status'] = False

        return results


class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    friends = models.ManyToManyField('self')
    objects = UserManager()
    