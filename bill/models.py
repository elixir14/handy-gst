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

    account_number = models.CharField(max_length=25, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)
    pan = models.CharField(max_length=10, null=False, blank=False)

    remarks = models.CharField(max_length=200, blank=True)
    terms = models.TextField(default='', null=True, blank=True)
    authorised_signatory = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.invoice_no


class Item(models.Model):
    invoice = models.ForeignKey(Invoice)
    description = models.CharField(max_length=100)
    hsn_code = models.CharField(max_length=10, null=True, blank=True)
    quantity_code = models.CharField(max_length=10, null=True, blank=True)
    quantity = models.FloatField(default=0.0)
    rate = models.FloatField(default=0.0)
    value = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.description
