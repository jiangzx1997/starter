from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.TextField(max_length = 20)
    number = models.TextField(max_length = 8)

class Group(models.Model):
    name = models.CharField(max_length = 10)
    text = models.TextField()
    leader = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'LeadGroup')
    member = models.ManyToManyField(User)

'''
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
'''
