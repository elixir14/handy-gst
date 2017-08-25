from django import forms

from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, help_text='Required.')
    gst = forms.CharField(max_length=50, required=True, help_text='Required.')
    remarks = forms.CharField(max_length=200, required=False, help_text='Optional.')
    terms = forms.Textarea()
    authorised_signatory = forms.CharField(max_length=200, required=False, help_text='Optional.')

    class Meta:
        model = CompanyProfile
        fields = (
            'name', 'gst', 'remarks', 'terms', 'authorised_signatory',)

    def __unicode__(self):
        return self.name
