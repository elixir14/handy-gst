from django.conf.urls import url

from bill import views
urlpatterns = [
    url(r'^add/$', views.ItemCreate.as_view(success_url='bill_details'), name='add_bill'),
    url(r'^bill_details/$', views.InvoiceList.as_view(), name='bill-list'),
    url(r'^add/company_detail/$', views.company_detail, name='company_detail'),
    url(r'^add/client_detail/$', views.client_detail, name='client_detail')
]
