from django.contrib import admin

# Register your models here.
from ddl.models import Topic, GroupTask

admin.site.register(Topic)
admin.site.register(GroupTask)
