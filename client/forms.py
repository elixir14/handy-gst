from django import forms

from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, help_text='Required.')
    GST = forms.CharField(max_length=50, required=True, help_text='Required.')
    PAN = forms.CharField(max_length=50, required=False, help_text='Optional.')
    CGST = forms.CharField(max_length=50, required=False, help_text='Optional.')
    SGST = forms.CharField(max_length=50, required=False, help_text='Optional.')
    IGST = forms.CharField(max_length=50, required=False, help_text='Optional.')
    address = forms.Textarea()
    city = forms.CharField(max_length=100, required=False, help_text='Optional.')
    state = forms.CharField(max_length=50, required=False, help_text='Optional.')
    zip = forms.CharField(max_length=50, required=False, help_text='Optional.')
    first_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    phone_number = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=50, required=False, help_text='Optional.')
    bank_name = forms.CharField(max_length=200, required=False, help_text='Optional.')
    account_number = forms.CharField(max_length=50, required=False, help_text='Optional.')
    IFSC = forms.CharField(max_length=50, required=False, help_text='Optional.')
    remarks = forms.CharField(max_length=200, required=False, help_text='Optional.')
    terms = forms.Textarea()
    authorise = forms.CharField(max_length=200, required=False, help_text='Optional.')

    class Meta:
        model = CompanyProfile
        exclude = ('customer',)
        fields = (
            'name', 'GST', 'PAN', 'CGST', 'SGST', 'IGST', 'address', 'city', 'state', 'zip', 'first_name', 'last_name', 'phone_number', 'email', 'bank_name',
            'account_number', 'IFSC', 'remarks',
            'terms', 'authorise',)

    def __unicode__(self):
        return self.name
