from __future__ import unicode_literals, absolute_import
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from customer.forms import EditAddressForm, EditContactForm
from django.shortcuts import render
from .models import CompanyProfile
from .forms import ClientProfileForm
from customer.models import State
from client.models import ClientProfile

@login_required
def client_profile(request):
    companies = CompanyProfile.objects.all().order_by('name')
    state = State.objects.all().order_by('name')
    if request.method == 'POST':
        # print request.POST
        client_form = ClientProfileForm(request.POST or None)
        contact_form = EditContactForm(request.POST or None)
        billing_address_form = EditAddressForm(request.POST or None)
        shipping_address_form = EditAddressForm(request.POST or None)
        if (request.POST and client_form.is_valid() and contact_form.is_valid() and
                shipping_address_form.is_valid() and billing_address_form.is_valid()):
            contact_instance = contact_form.save()
            billing_address_instance = billing_address_form.save()
            shipping_address_instance = shipping_address_form.save()
            profile = client_form.save(commit=False)
            profile.contact = contact_instance
            profile.billing_address = billing_address_instance
            profile.shipping_address = shipping_address_instance
            profile.save()
            return HttpResponseRedirect("/client/list/")
        else:
            # print ("else")
            print client_form.errors
            print contact_form.errors
            print billing_address_form.errors
            print shipping_address_form.errors
    else:
        client_form = ClientProfileForm()
    data = {'form': client_form, 'companies': companies, 'states': state}
    return render(request, 'frontend/client_profile.html', data)


@login_required
def client_view(request):
    clients = ClientProfile.objects.all()
    data = {
        'clients': clients
    }
    return render(request, 'frontend/client_view_profile.html', context=data)


@login_required
def client_remove(request, id=None):
    # client = ClientProfile.objects.get(pk=id)
    # client.delete()
    clients = []    # ClientProfile.objects.all()
    data = {
        'clients': clients
    }
    return render(request, 'frontend/company_view_profile.html', context=data)


@login_required
def client_remove(request, id=None):
    pass



