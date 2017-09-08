from __future__ import unicode_literals, absolute_import
import json

from .models import Invoice, Item
from django.forms import inlineformset_factory, ModelForm
from django import forms

from company.models import CompanyProfile
from client.models import ClientProfile
from customer.models import State


class InvoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        for item in ['company', 'billing_state', 'shipping_state']:
            if item in kwargs.keys():
                kwargs.pop(item)
        user = kwargs.pop('user')
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = CompanyProfile.objects.filter(customer__user=user)
        self.fields['billing_state'].choices = tuple([("", "-- Select State --")] +
                                                     [(state.name, state.name)for state in State.objects.all()])
        self.fields['shipping_state'].choices = tuple([("", "-- Select State --")] +
                                                     [(state.name, state.name) for state in State.objects.all()])

    company = forms.ModelChoiceField(queryset=CompanyProfile.objects.none(),  empty_label="-- Select Company --",
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    client = forms.ModelChoiceField(queryset=ClientProfile.objects.all(), empty_label="-- Select Client --",
                                    widget=forms.Select(attrs={'class':'form-control'}))
    client_gst = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label='GSTIN / UIN')
    invoice_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    invoice_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipient = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                label="Recipient Name")
    consignee = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                label="Consignee Name")
    billing_address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}), label="Billing Address")
    billing_state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Billing State")
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}), label="Shipping Address")
    shipping_state = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), label="Shipping State")
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     label="Bank Account Number")
    ifsc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Bank IFSC Code")
    pan = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="PAN Number")
    remarks = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    terms = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '1', 'class': 'form-control'}),
        label="Terms and Conditions", required=False)
    authorised_signatory = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           required=False, label="Authorised Signatory")
    cgst = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'onKeyup': "Test();"}),
                            required=False, label="CGST")
    sgst = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'onKeyup': "Test();"}),
                            required=False, label="SGST")
    igst = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'onKeyup': "Test();"}),
                            required=False, label="IGST")
    total = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readOnly': 'True'}),
                            required=False, label="Total")
    gst_amount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readOnly': 'True'}),
                            required=False, label="Tax Amount: GST")

    grand_total = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'readOnly': 'True'}),
                             required=False, label="Total Amount After Tax")

    cgst_total = forms.FloatField(widget=forms.HiddenInput())
    sgst_total = forms.FloatField(widget=forms.HiddenInput())
    igst_total = forms.FloatField(widget=forms.HiddenInput())
    billing_state_code = forms.CharField(widget=forms.HiddenInput())
    shipping_state_code = forms.CharField(widget=forms.HiddenInput())


    class Meta:
        model = Invoice
        exclude = ()
        fields = ('company', 'client', 'invoice_no','invoice_date', 'recipient', 'consignee', 'billing_address',
                  'shipping_address', 'billing_state', 'shipping_state', 'authorised_signatory', 'client_gst',
                  'account_number', 'cgst' , 'ifsc', 'sgst', 'pan', 'igst', 'remarks', 'gst_amount', 'terms' ,'total',
                  'grand_total', 'shipping_state_code', 'billing_state_code', 'cgst_total', 'sgst_total', 'igst_total')


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
                                 required=False, label="Taxable Value")

    class Meta:
        model = Item
        exclude = ()
        fields = ('description', 'hsn_code', 'quantity_code', 'quantity', 'rate', 'value', 'discount', 'tax_value')

ItemFormSet = inlineformset_factory(Invoice, Item, form=ItemForm, extra=1)
