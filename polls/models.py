# coding=utf-8

import datetime
from django.db import models
from django.utils import timezone
from django import forms
# from django.contrib import auth
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):              # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)

    def __unicode__(self):              # __unicode__ on Python 2
        return self.choice_text


class Vote(models.Model):
    question = models.CharField(max_length=200)
    choice = models.ForeignKey(Choice)
    user = models.CharField(max_length=30)
    vote_time = models.DateField()



