from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# tUserProfile is an extention of the auth_user table,
# hence the OneToOneField relationship
class tUserProfile(models.Model):
	user   = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.FileField(upload_to='media/', blank=True, null=True)
	subscr = models.BooleanField(default=False)

	class Meta:
		verbose_name        = 'User Profile'
		verbose_name_plural = 'User Profiles'

	def __str__(self):
		return str(self.user)

# The following two procs behave as triggers in auth_user
# Since tUserProfile is an extention of auth_user, we need
# to monitor it for changes. i.e if a new user is added,
# we need to create a new tUserProfile entry as well. 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		tUserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.tuserprofile.save()

