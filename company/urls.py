from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.company_profile, name='profile'),
    url(r'^list/$', views.company_view, name='company_view'),
    url(r'^delete/(?P<id>\d+)$', views.company_remove, name='company_remove'),
]
