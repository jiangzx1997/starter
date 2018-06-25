from django.contrib import admin

# Register your models here.
from users.models import MyUser, Group

admin.site.register(MyUser)
admin.site.register(Group)