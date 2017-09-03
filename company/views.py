from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from customer.forms import EditAddressForm, EditContactForm, EditBankForm, EditTaxForm
from customer.models import State, CustomerProfile
from .forms import CompanyProfileForm
from .models import CompanyProfile


@login_required
def company_profile(request):
    state = State.objects.all().order_by('name')
    if request.method == 'POST':
        company_form = CompanyProfileForm(request.POST or None)
        contact_form = EditContactForm(request.POST or None)
        address_form = EditAddressForm(request.POST or None)
        bank_form = EditBankForm(request.POST or None)
        tax_form = EditTaxForm(request.POST or None)
        for item in [company_form, contact_form, address_form, bank_form, tax_form]:
            if not item.is_valid():
                return render(request, 'frontend/company_profile.html',
                              {'form': company_form, 'states': state, 'error_message': item.errors})
        if (request.POST and company_form.is_valid() and contact_form.is_valid() and
                address_form.is_valid() and bank_form.is_valid() and tax_form.is_valid()):
            print (request.user.id)
            contact_instance = contact_form.save()
            profile = company_form.save(commit=False)
            address_instance = address_form.save()
            bank_instance = bank_form.save()
            tax_instance = tax_form.save()
            profile.contact = contact_instance
            profile.address = address_instance
            profile.bank_detail = bank_instance
            profile.tax_detail = tax_instance
            profile.customer = CustomerProfile.objects.get(user=request.user.id)
            profile.save()
            return HttpResponseRedirect("/company/list/")
    else:
        company_form = CompanyProfileForm()
    return render(request, 'frontend/company_profile.html', {'form': company_form, 'states': state})


@login_required
def company_view(request):
    companies = CompanyProfile.objects.filter(customer__user=request.user)
    data = {
        'profile': companies
    }
    return render(request, 'frontend/company_view_profile.html', context=data)


@login_required
def company_remove(request, id):
    company = CompanyProfile.objects.get(pk=id)
    company.delete()
    companies = CompanyProfile.objects.all()
    data = {
        'profile': companies
    }
    return render(request, 'frontend/company_view_profile.html', context=data)


@login_required
def company_edit(request, id=None):
    state = State.objects.all().order_by('name')
    profile = get_object_or_404(CompanyProfile, pk=id)
    if request.method == 'POST':
        company_form = CompanyProfileForm(request.POST or None, instance=profile)
        contact_form = EditContactForm(request.POST or None, instance=profile.contact)
        address_form = EditAddressForm(request.POST or None, instance=profile.address)
        bank_form = EditBankForm(request.POST or None, instance=profile.bank_detail)
        tax_form = EditTaxForm(request.POST or None, instance=profile.tax_detail)
        if request.POST and company_form.is_valid() and contact_form.is_valid() and address_form.is_valid() and bank_form.is_valid() and tax_form.is_valid():
            contact_instance = contact_form.save()
            profile = company_form.save(commit=False)
            address_instance = address_form.save()
            bank_instance = bank_form.save()
            tax_instance = tax_form.save()
            profile.contact = contact_instance
            profile.address = address_instance
            profile.bank_detail = bank_instance
            profile.tax_detail = tax_instance
            profile.customer = CustomerProfile.objects.get(user=request.user.id)
            profile.save()
            return HttpResponseRedirect("/company/list/")

    return render(request, 'frontend/company_profile.html', {'profile': profile, 'states': state})
