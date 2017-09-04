from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from common.base_model import HandyBase
from .constants import CustomerStatus


class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = "gst_state"

    def __unicode__(self):
        return self.name


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
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=25, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "gst_bank"

    def __unicode__(self):
        return self.bank_name


class Tax(HandyBase):
    pan = models.CharField(max_length=10, null=False, blank=False)
    cgst = models.FloatField(default=0.00, null=True)
    sgst = models.FloatField(default=0.00, null=True)
    igst = models.FloatField(default=0.00, null=True)

    class Meta:
        db_table = "gst_tax"

    def __unicode__(self):
        return self.pan


class Contact(HandyBase):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'."
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    fax_number = RegexValidator(regex=r'^\d+$',
                                message="Fax number must be entered in the number.")
    fax_number = models.CharField(validators=[fax_number], max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "gst_contact"

    def __unicode__(self):
        return self.address


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    status = models.SmallIntegerField(choices=CustomerStatus.FieldStr.items(), default=CustomerStatus.Pending)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "gst_customer_profile"

    def __unicode__(self):
        return self.user.username
