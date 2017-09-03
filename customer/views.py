from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from customer.models import CustomerProfile, State
from .forms import EditCustomerForm, EditContactForm, EditAddressForm


@login_required
def customer_profile(request):
    profile = get_object_or_404(CustomerProfile, user=request.user.id)
    state = State.objects.all().order_by('name')
    return render(request, 'frontend/customer_profile.html', {'profile': profile, 'states': state})


@login_required
def edit_customer_profile(request, id=None):
    if id:
        state = State.objects.all().order_by('name')
        profile = get_object_or_404(CustomerProfile, pk=id)
        customer_form = EditCustomerForm(request.POST or None, instance=profile)
        contact_form = EditContactForm(request.POST or None, instance=profile.contact)
        address_form = EditAddressForm(request.POST or None, instance=profile.address)
        for item in [customer_form, contact_form, contact_form, address_form]:
            if not item.is_valid():
                return render(request, 'frontend/customer_profile.html',
                              {'profile': profile, 'states': state,
                               'error_message': item.errors})
        if request.POST and customer_form.is_valid() and contact_form.is_valid() and address_form.is_valid():
            contact_instance = contact_form.save()
            profile = customer_form.save(commit=False)
            address_instance = address_form.save()
            profile.contact = contact_instance
            profile.address = address_instance
            profile.save()
            return render(request, 'frontend/customer_profile.html',
                          {'profile': profile, 'states': state, 'message': 'Profile updated successfully.'})

    return render(request, 'frontend/customer_profile.html', {'error_message': 'Failed to updated profile.'})
