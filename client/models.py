from __future__ import unicode_literals, absolute_import

from django.db import models
from django.db.models import Value as V
from django.db.models.functions import Concat

from common.base_model import HandyBase
from company.models import CompanyProfile
from customer.models import Address, Contact
from common.login_user import get_current_user


class ClientManager(models.Manager):
    def get_queryset(self):
        return super(ClientManager, self).get_queryset().filter(company__customer__user=get_current_user())

    def get_display(self):
        return self.annotate(
            display_name=Concat('client_name', V(' ('), 'gst', V(')'))).all().order_by('client_name')


class ClientProfile(HandyBase):
    objects = ClientManager()
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100, null=False, blank=False)
    gst = models.CharField(max_length=50, null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='billing_address')
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='shipping_address')
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "gst_client_profile"

    def __unicode__(self):
        return self.client_name
