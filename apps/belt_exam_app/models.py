from __future__ import unicode_literals
from ..loginRegistration_app.models import User
from django.db import models

class QuoteManager(models.Manager):
    def create_qt(self, postData, u_id):
        error_list = []
        if postData['qtd_by'] < 4 or postData['msg'] < 11:
            error_list.append('Enter Quoted by and Message')
            context = {'status':0, 'errors':error_list}
            return context
        else:
            usr = User.objects.get(id = u_id)
            self.create(quote = postData['msg'], quoted_by = postData['qtd_by'], creator = usr)
            context = {'status':1}
            return context

    def add(self, q_id, u_id):
        usr = User.objects.get(id = u_id)
        qt = self.get(id = q_id)
        qt.likes.add(usr)

    def remove(self, q_id, u_id):
        usr = User.objects.get(id = u_id)
        qt = self.get(id = q_id)
        qt.likes.remove(usr)

class Quote(models.Model):
    quote = models.TextField(max_length = 500)
    creator = models.ForeignKey(User, related_name = 'all_quotes')
    quoted_by = models.CharField(max_length = 100)
    likes = models.ManyToManyField(User, related_name = 'all_users')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = QuoteManager()
# Create your models here.
