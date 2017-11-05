# Django imports
from django.db import models


class tHomeContent(models.Model):
    """ Stores the home content """

    text = models.TextField()

    class Meta:
        verbose_name = 'Home content'
        verbose_name_plural = 'Home content'
