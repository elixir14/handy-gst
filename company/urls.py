from django.conf.urls import url
from django.views.generic import ListView
from . import views
from .models import CompanyProfile
urlpatterns = [
    url(r'^add/$', views.company_profile, name='profile'),
    url(r'^list/$', views.company_view, name='company_view'),
    url(r'^delete/(?P<id>\d+)$', views.company_remove, name='company_remove'),
    url(r'^edit/(?P<id>\d+)$', views.company_edit, name='company_edit'),
]
