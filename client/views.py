from __future__ import unicode_literals, absolute_import
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from customer.forms import EditAddressForm, EditContactForm
from django.shortcuts import render, get_object_or_404
from .models import CompanyProfile
from .forms import ClientProfileForm
from customer.models import State
from client.models import ClientProfile
from django.contrib import messages


@login_required
def client_profile(request):
    companies = CompanyProfile.objects.filter(customer__user=request.user)
    state = State.objects.all().order_by('name')
    if request.method == 'POST':
        # print request.POST
        client_form = ClientProfileForm(request.POST or None)
        contact_form = EditContactForm(request.POST or None)
        addresses = {"shipping": {}, "billing": {}}
        for type in addresses.keys():
            for item in ['address', 'city', 'state', 'zip']:
                addresses[type][item] = request.POST[type + "_" + item]

        billing_address_form = EditAddressForm(addresses['billing'] or None)
        shipping_address_form = EditAddressForm(addresses['shipping'] or None)

        for item in [client_form, contact_form, billing_address_form, shipping_address_form]:
            if not item.is_valid():
                print item.errors
                return render(request, 'frontend/client_profile.html',
                              {'form': client_form, 'states': state, 'error_message': item.errors})
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
        client_form = ClientProfileForm()
    data = {'form': client_form, 'companies': companies, 'states': state}
    return render(request, 'frontend/client_profile.html', data)


@login_required
def update_client_profile(request, id):
    companies = CompanyProfile.objects.filter(customer__user=request.user)
    state = State.objects.all().order_by('name')
    profile = get_object_or_404(ClientProfile, pk=id)
    if request.method == 'POST':
        # print request.POST
        client_form = ClientProfileForm(request.POST or None, instance=profile)
        contact_form = EditContactForm(request.POST or None, instance=profile.contact)
        addresses = {"shipping": {}, "billing": {}}
        for type in addresses.keys():
            for item in ['address', 'city', 'state', 'zip']:
                addresses[type][item] = request.POST[type + "_" + item]

        billing_address_form = EditAddressForm(addresses['billing'] or None, instance=profile.billing_address)
        shipping_address_form = EditAddressForm(addresses['shipping'] or None, instance=profile.shipping_address)
        for item in [client_form, contact_form, billing_address_form, shipping_address_form]:
            if not item.is_valid():
                print item.errors
                return render(request, 'frontend/client_profile.html',
                              {'form': client_form, 'states': state, 'companies': companies,
                               'error_message': item.errors, 'profile': profile})
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
        client_form = ClientProfileForm()
    data = {'form': client_form, 'companies': companies, 'states': state, 'profile': profile}
    return render(request, 'frontend/client_profile.html', data)


@login_required
def client_view(request):
    clients = ClientProfile.objects.filter(company__customer__user=request.user)
    data = {
        'clients': clients
    }
    return render(request, 'frontend/client_view_profile.html', context=data)


@login_required
def client_remove(request, id):
    client = ClientProfile.objects.get(pk=id)
    client.delete()
    clients = ClientProfile.objects.filter(company__customer__user=request.user)
    data = {
        'clients': clients
    }
    return render(request, 'frontend/client_view_profile.html', context=data)
