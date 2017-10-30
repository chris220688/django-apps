# Django imports
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class tUserProfile(models.Model):
    """ Extends auth_user table, hence the OneToOneField relationship """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='media/', blank=True, null=True)
    subscr = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Function that behaves as a trigger in auth_user.

        tUserProfile is an extention of auth_user. If a new
        user is added, a new tUserProfile entry needs to be created.
    """

    if created:
        tUserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ Function that behaves as a trigger in auth_user.

        tUserProfile is an extention of auth_user. Any changes
        in auth_user need to be reflected in tUserProfile.
    """

    instance.tuserprofile.save()
