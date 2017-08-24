from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^profile/$', views.customer_profile, name='profile'),
    url(r'^profile/(?P<id>\d+)/$', views.edit_customer_profile, name='profile'),
]
