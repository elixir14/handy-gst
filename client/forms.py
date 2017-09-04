from django import forms

from .models import ClientProfile
from company.models import CompanyProfile


class ClientProfileForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=CompanyProfile.objects.all())
    client_name = forms.CharField(max_length=100, required=True, help_text='Required.')
    gst = forms.CharField(max_length=50, required=False, help_text='Required.')
    remarks = forms.CharField(max_length=200, required=False, help_text='Optional.')

    class Meta:
        model = ClientProfile
        fields = ('company', 'client_name', 'gst','remarks')

    def __unicode__(self):
        return self.client_name
