from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

app_name = 'users'
urlpatterns = [
    # login page
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name = 'login'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^group/$', views.group, name = 'group'),
    url(r'^new_group/$', views.new_group, name = 'new_group'),
    url(r'^choose_member/(?P<group_id>\d+)/$', views.add_member, name = 'change_member'),
    url(r'^del_member/(?P<group_id>\d+)/(?P<user_number>\d+)/$', views.del_member, name = 'del_member'),
    url(r'^edit_group/(?P<group_id>\d+)/$', views.edit_group, name = 'edit_group'),
]
