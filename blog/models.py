# Standard library imports
import datetime

# Django imports
from django.contrib.auth.models import User
from django.db import models


class tPost(models.Model):
    """ Stores post entries """

    author = models.ForeignKey(User)
    title = models.CharField(max_length=128)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class tComment(models.Model):
    """ Stores comments entries """

    user = models.ForeignKey(User)
    post = models.ForeignKey(tPost, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)

class tLike(models.Model):
    """ Stores like entries """

    user = models.ForeignKey(User)
    post = models.ForeignKey(tPost, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
