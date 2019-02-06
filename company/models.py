from __future__ import unicode_literals, absolute_import

from django.db import models
from django.db.models import Value as V
from django.db.models.functions import Concat

from common.base_model import HandyBase
from common.login_user import get_current_user
from customer.models import CustomerProfile, Address, Bank, Tax, Contact


class CompanyManager(models.Manager):
    def get_queryset(self):
        return super(CompanyManager, self).get_queryset().filter(customer__user=get_current_user())

    def get_display(self):
        return self.annotate(
            display_name=Concat('company_name', V(' ('), 'gst', V(')'))).all().order_by('company_name')


class CompanyProfile(HandyBase):
    objects = CompanyManager()
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=False, blank=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    gst = models.CharField(max_length=50, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    bank_detail = models.ForeignKey(Bank, on_delete=models.CASCADE)
    tax_detail = models.ForeignKey(Tax, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200, blank=True)
    terms = models.TextField(default='', null=True, blank=True)
    authorised_signatory = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "gst_company_profile"

    def __unicode__(self):
        return self.company_name
