from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class CompanyProfile(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    GST = models.CharField(max_length=50, null=False, blank=False)
    address = models.TextField(default='', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    juridiction_text = models.CharField(max_length=200, blank=True)
    note = models.TextField(default='', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bill_company_profile"

    def __unicode__(self):
        return self.name
