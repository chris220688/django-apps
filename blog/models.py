from django.db import models
from django.contrib.auth.models import User
import datetime

class tPost(models.Model):
	author = models.ForeignKey(User)
	title  = models.CharField(max_length=128)
	text   = models.TextField()
	date   = models.DateTimeField(default=datetime.datetime.now)

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'

class tComment(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(tPost, on_delete=models.CASCADE)
	text = models.TextField()
	date = models.DateTimeField(default=datetime.datetime.now)

class tLike(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(tPost, on_delete=models.CASCADE)
	date = models.DateTimeField(default=datetime.datetime.now)
