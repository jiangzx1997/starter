from django.conf.urls import url

from . import views

app_name = 'ddl'
urlpatterns = [
    # home page
    url(r'^$', views.index, name = 'index'),
    
    # show all item
#    url(r'^topics/$', views.topics, name = 'topics'),
    
    # ?????????
    url(r'^topic/$', views.topic, name = 'topic'),
    
    # add new topic
#    url(r'^new_topic/$', views.new_topic, name = 'new_topic'),
    
    # add new entry
    url(r'^new_entry/$', views.new_entry, name = 'new_entry'),
    
    # edit entry
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name = 'edit_entry'),

    # delete entry
    url(r'^delete_entry/(?P<entry_id>\d+)/$', views.delete_entry, name = 'delete_entry'),

    # finish entry
    url(r'^finish_entry/(?P<entry_id>\d+)/$', views.finish_entry, name = 'finish_entry'),
]
