from __future__ import unicode_literals, absolute_import
import json

from .models import Invoice, Item
from django.forms import inlineformset_factory, ModelForm
from django import forms

from .constants import ReportingPreference
from company.models import CompanyProfile
from client.models import ClientProfile


class InvoiceForm(ModelForm):
    dclients = {}
    list_clients = []
    for client_obj in ClientProfile.objects.all():
        if client_obj.client() in dclients:
            dclients[client_obj.client()].append(client_obj.name)
        else:
            dclients[client_obj.client()] = [client_obj.name]
        list_clients.append((client_obj.id, client_obj.name))

    companies = {}
    for company in CompanyProfile.objects.all():
        companies[company.id] = company.name

    brand_select = forms.ChoiceField(choices=([(company.id, company.name) for company in CompanyProfile.objects.all()]),
                                     widget=forms.Select(attrs={"class": "form-control"}), label="Select Company")
    car_select = forms.ChoiceField(choices=list_clients, widget=forms.Select(attrs={"class": "form-control"}),
                                   label="Select Client")

    companies = json.dumps(companies)
    clients = json.dumps(dclients)

    gst = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label='GSTN/UIN')
    invoice_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    invoice_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))

    recipient = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                label="Recipient Name")
    consignee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                label="Consignee Name")
    bill_for = forms.ChoiceField(choices=ReportingPreference.FieldStr.items(),
                                 widget=forms.Select(attrs={"class": "form-control"}), label="Bill Preference")
    billing_address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}), label="Billing Address")

    bill_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State")
    bill_state_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State Code")

    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}), label="Shipping Address")
    shipping_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State")
    shipping_state_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State Code")

    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     label="Bank Account Number")
    ifsc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Bank IFSC Code")
    pan = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="PAN Number")

    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    terms = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}),
        label="Terms and Conditions", required=False)
    authorised_signatory = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Invoice
        exclude = ()
        fields = ('brand_select', 'car_select', 'invoice_no', 'bill_for', 'gst', 'recipient', 'billing_address',
                  'bill_state','bill_state_code', 'consignee','shipping_address', 'shipping_state',
                  'shipping_state_code','remarks', 'terms', 'authorised_signatory', 'account_number', 'ifsc', 'pan' )


class ItemForm(ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    hsn_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}),label="HSN/ACS", required=False)
    quantity_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' } ), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numeric', 'onKeyup' : "Test();"}), required=True)
    rate = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numeric', 'onKeyup' : "Test();"}), required=True)
    value = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly' : 'True'}), required=True)
    discount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numeric', 'onKeyup' : "Test();"}))

    class Meta:
        model = Item
        exclude = ()
        fields = ('description', 'hsn_code', 'quantity_code', 'quantity', 'rate', 'value', 'discount')


ItemFormSet = inlineformset_factory(Invoice, Item, form=ItemForm, extra=1)
