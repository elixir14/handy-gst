from django import forms

from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, help_text='Required.')
    GST = forms.CharField(max_length=50, required=True, help_text='Required.')
    address = forms.Textarea()
    city = forms.CharField(max_length=100, required=False, help_text='Optional.')
    state = forms.CharField(max_length=50, required=False, help_text='Optional.')
    zip = forms.CharField(max_length=50, required=False, help_text='Optional.')
    first_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    phone_number = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=50, required=False, help_text='Optional.')
    juridiction_text = forms.CharField(max_length=200, required=False, help_text='Optional.')
    note = forms.Textarea()

    class Meta:
        model = CompanyProfile
        exclude = ('customer',)
        fields = ('name', 'GST', 'address', 'city', 'state', 'zip', 'first_name', 'last_name', 'phone_number', 'email', 'juridiction_text', 'note',)

    def __unicode__(self):
        return self.name
