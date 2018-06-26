from django.db import models
from django.contrib.auth.models import User
from users.models import Group

# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.text


class Entry(models.Model):
#    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    YYYY = models.IntegerField()
    MM = models.IntegerField()
    DD = models.IntegerField()
    date_ended = models.DateTimeField()
    text = models.TextField()
    tag = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add = True)
    title = models.TextField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.text[:50] + "..."

class GroupTask(models.Model):
    YYYY = models.IntegerField()
    MM = models.IntegerField()
    DD = models.IntegerField()
    date_ended = models.DateTimeField()
    text = models.TextField()
    tag = models.BooleanField()
    date_added = models.DateTimeField(auto_now_add = True)
    title = models.TextField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    