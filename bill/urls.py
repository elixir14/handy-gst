from django.conf.urls import url

from bill import views

urlpatterns = [
    url(r'^add/$', views.ItemCreate.as_view(), name='add_bill'),
]
