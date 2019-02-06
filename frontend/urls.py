from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^customer/', include('customer.urls', namespace='customer')),
    url(r'^company/', include('company.urls', namespace='company')),
    url(r'^client/', include('client.urls', namespace='client')),
    url(r'^bill/', include('bill.urls', namespace='bill')),
]
