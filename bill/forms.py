from __future__ import unicode_literals, absolute_import
import json

from .models import Invoice, Item
from django.forms import inlineformset_factory, ModelForm
from django import forms

from .constants import ReportingPreference
from company.models import CompanyProfile
from client.models import ClientProfile


class InvoiceForm(ModelForm):
    company = forms.ChoiceField(choices=([('', '-- Select Company --')] +
                                         [(company.id, "%s (%s)" % (company.company_name, company.gst)) for company in
                                          CompanyProfile.objects.all()]),
                                widget=forms.Select(attrs={"class": "form-control"}), label="Select Company")
    client = forms.ChoiceField(choices=([('', '-- Select Client --')]),
                               widget=forms.Select(attrs={"class": "form-control"}),
                               label="Select Client")

    client_gst = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label='GSTN/UIN')
    invoice_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    invoice_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%'}))

    recipient = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                label="Recipient Name")
    consignee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                label="Consignee Name")
    # bill_for = forms.ChoiceField(choices=ReportingPreference.FieldStr.items(),
    #                              widget=forms.Select(attrs={"class": "form-control"}), label="Bill Preference")
    billing_address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}), label="Billing Address")

    billing_state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State")
    billing_state_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="State Code")

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

    cgst = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label="CGST")
    sgst = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label="SGST")
    igst = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False, label="IGST")

    total = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readOnly': 'True'}),
                             required=False,
                             label="Amount to Paid")

    class Meta:
        model = Invoice
        exclude = ()
        fields = ('company', 'client', 'invoice_no', 'client_gst', 'recipient', 'billing_address',
                  'billing_state', 'billing_state_code', 'consignee', 'shipping_address', 'shipping_state',
                  'shipping_state_code', 'remarks', 'terms', 'authorised_signatory', 'account_number', 'ifsc', 'pan',
                  'cgst', 'sgst', 'igst', 'total')


class ItemForm(ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "style": "width:250px"}),
                                  required=True)
    hsn_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control '}), label="HSN/ACS",
                               required=False)
    quantity_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control col-xs-2', 'onKeyup': "Test();"}),
                                required=True)
    rate = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numeric', 'onKeyup': "Test();"}),
                            required=True)
    value = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
                             required=False)
    discount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numeric', 'onKeyup': "Test();"}),
                                required=False)
    tax_value = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
                                 required=False)

    class Meta:
        model = Item
        exclude = ()
        fields = ('description', 'hsn_code', 'quantity_code', 'quantity', 'rate', 'value', 'discount')

ItemFormSet = inlineformset_factory(Invoice, Item, form=ItemForm, extra=1)
