from __future__ import unicode_literals

from django.db import models

from customer.models import Address
from company.models import CompanyProfile
from client.models import ClientProfile

from constants import ReportingPreference


class Invoice(models.Model):
    gst = models.CharField(max_length=50, null=False, blank=False)
    invoice_no = models.CharField(max_length=100)
    invoice_date = models.DateField(auto_now_add=True)
    recipient = models.CharField(max_length=100)
    consignee = models.CharField(max_length=100)
    bill_for = models.IntegerField(choices=ReportingPreference.FieldStr.items(), default=ReportingPreference.for_recipient)
    billing_address = models.TextField(default='')
    shipping_address = models.TextField(default='')


    def __unicode__(self):
        return None


class Item(models.Model):
    invoice = models.ForeignKey(Invoice)
    description = models.CharField(max_length=100)
    quantity = models.IntegerField()
    rate = models.IntegerField()
    value = models.IntegerField()
    # discount = models.SmallIntegerField()
    # total = models.FloatField()


