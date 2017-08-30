from __future__ import unicode_literals, absolute_import

from django.forms import inlineformset_factory, ModelForm
from .models import Invoice, Item
from django import forms
from .constants import ReportingPreference


class InvoiceForm(ModelForm):
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
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}),
        label="Billing Address")
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '2', 'rows': '2', 'class': 'form-control'}),
        label="Shipping Address")

    class Meta:
        model = Invoice
        exclude = ()
        fields = ('invoice_no', 'bill_for', 'gst', 'recipient', 'billing_address', 'consignee', 'shipping_address',)


class ItemForm(ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    rate = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    value = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Item
        exclude = ()
        fields = ('description', 'quantity', 'rate', 'value')


ItemFormSet = inlineformset_factory(Invoice, Item, form=ItemForm, extra=1)
