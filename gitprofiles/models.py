from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers= models.IntegerField(null=True)
    last_updated=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Repository(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    repo_name=models.TextField(null=True)
    stars=models.IntegerField(null=True)
    def __str__(self):
        return self.name


    

