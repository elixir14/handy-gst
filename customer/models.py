from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.base_model import HandyBase


class State(models.Model):
    state = models.CharField(max_length=50)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = "gst_state"

    def __unicode__(self):
        return self.state


# Create your models here.
class Address(HandyBase):
    address = models.TextField(default='', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    state = models.ForeignKey(State)

    class Meta:
        db_table = "gst_address"

    def __unicode__(self):
        return self.address


class Bank(HandyBase):
    name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=25, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "gst_bank"

    def __unicode__(self):
        return self.address


class Tax(HandyBase):
    pan = models.CharField(max_length=10, null=False, blank=False)
    cgst = models.FloatField(default=0.00)
    sgst = models.FloatField(default=0.00)
    igst = models.FloatField(default=0.00)

    class Meta:
        db_table = "gst_tax"

    def __unicode__(self):
        return self.gst


class Contact(HandyBase):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    fax_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "gst_contact"

    def __unicode__(self):
        return self.address


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gst_customer_profile"

    def __unicode__(self):
        return self.user.username
