from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.client_profile, name='profile'),
    url(r'^list/$', views.client_view, name='client_view'),
    url(r'^edit/(?P<id>\d+)$', views.client_edit, name='client_edit'),
    url(r'^delete/(?P<id>\d+)$', views.client_remove, name='client_remove'),
]
