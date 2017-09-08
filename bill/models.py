from __future__ import unicode_literals

from django.db import models
from company.models import CompanyProfile
from client.models import ClientProfile
from common.Sample import get_current_user


class InvoiceManager(models.Manager):
    def get_queryset(self):
        return super(InvoiceManager, self).get_queryset().filter(company__customer__user=get_current_user())

    def for_user(self, user):
        return super(InvoiceManager, self).get_queryset().filter(company__customer__user=user)



class Invoice(models.Model):
    # objects = InvoiceManager()
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    client_gst = models.CharField(max_length=50, null=False, blank=False)
    invoice_no = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    recipient = models.CharField(max_length=255)
    consignee = models.CharField(max_length=255)

    billing_address = models.TextField(default='')
    billing_state = models.CharField(max_length=50)
    billing_state_code = models.CharField(max_length=3)

    shipping_address = models.TextField(default='')
    shipping_state = models.CharField(max_length=50)
    shipping_state_code = models.CharField(max_length=3)

    account_number = models.CharField(max_length=25, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)
    pan = models.CharField(max_length=10, null=False, blank=True)

    cgst = models.FloatField(default=0.00, null=True)
    sgst = models.FloatField(default=0.00, null=True)
    igst = models.FloatField(default=0.00, null=True, blank=True)

    remarks = models.CharField(max_length=200, blank=True)
    terms = models.TextField(default='', null=True, blank=True)
    authorised_signatory = models.CharField(max_length=200, blank=True)
    total = models.FloatField(default=0.0)
    grand_total = models.FloatField(default=0.0)

    cgst_total = models.FloatField(default=0.0)
    sgst_total = models.FloatField(default=0.0)
    igst_total = models.FloatField(default=0.0)

    gst_amount = models.FloatField(default=0.0)

    class Meta:
        db_table = "gst_invoice"

    def __unicode__(self):
        return self.invoice_no


class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=False, blank=False)
    hsn_code = models.CharField(max_length=10, null=True, blank=True)
    quantity_code = models.CharField(max_length=10, null=True, blank=True)
    quantity = models.FloatField(default=0.0)
    rate = models.FloatField(default=0.0)
    value = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    tax_value = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.description

    class Meta:
        db_table = "gst_invoice_item"
