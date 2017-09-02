from __future__ import unicode_literals, absolute_import

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from customer.models import CustomerProfile, Contact, Address, State, Bank, Tax


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class EditCustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomerProfile
        fields = ('first_name', 'last_name', 'email')


class EditContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=False, help_text='Optional.')
    phone_number = forms.CharField(max_length=50, required=False, help_text='Optional.')
    fax_number = forms.CharField(max_length=50, required=False, help_text='Optional.')

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'fax_number')


class EditAddressForm(forms.ModelForm):
    address = forms.Textarea()
    city = forms.CharField(max_length=100, required=False, help_text='Optional.')
    zip = forms.CharField(max_length=50, required=False, help_text='Optional.')
    state = forms.ModelChoiceField(queryset=State.objects.all())

    class Meta:
        model = Address
        fields = ('address', 'city', 'zip', 'state')


class EditBankForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    account_number = forms.CharField(max_length=25, required=False, help_text='Optional.')
    ifsc = forms.CharField(max_length=15, required=False, help_text='Optional.')

    class Meta:
        model = Bank
        fields = ('name', 'account_number', 'ifsc')


class EditTaxForm(forms.ModelForm):
    pan = forms.CharField(max_length=10, required=False, help_text='Optional.')
    cgst = forms.FloatField(required=False)
    sgst = forms.FloatField(required=False)
    igst = forms.FloatField(required=False)

    class Meta:
        model = Tax
        fields = ('pan', 'cgst', 'sgst', 'igst')
