from django.conf.urls import url

from bill import views
urlpatterns = [
    url(r'^add/$', views.ItemCreate.as_view(success_url='bill_list'), name='add_bill'),
    # url(r'^bill_details/$', views.InvoiceList.as_view(), name='bill_details'),
    url(r'^bill_details/$', views.bill_list, name='bill_list'),
    url(r'^add/company_detail/$', views.company_detail, name='company_detail'),
    url(r'^add/client_detail/$', views.client_detail, name='client_detail'),
    url(r'edit/(?P<pk>[0-9]+)/$', views.ItemUpdate.as_view(), name='bill_list'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.bill_delete, name='bill_list'),
]
