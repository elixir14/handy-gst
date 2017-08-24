from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import CompanyProfileForm
from .models import CompanyProfile


@login_required
def company_profile(request):
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer = User.objects.get(pk=request.user.id)
            instance.save()
            return HttpResponseRedirect("/company/list/")
    else:
        form = CompanyProfileForm()
    return render(request, 'frontend/company_profile.html', {'form': form})


@login_required
def company_view(request):
    companies = CompanyProfile.objects.all()
    data = {
        'companyprofile': companies
    }
    return render(request, 'frontend/company_view_profile.html', context=data)


@login_required
def company_remove(request, id):
    company = CompanyProfile.objects.get(pk=id)
    company.delete()
    companies = CompanyProfile.objects.all()
    data = {
        'companyprofile': companies
    }
    return render(request, 'frontend/company_view_profile.html', context=data)


@login_required
def company_edit(request, id=None):
    if id:
        company = get_object_or_404(CompanyProfile, pk=id)
        form = CompanyProfileForm(request.POST or None, instance=company)
        if request.POST and form.is_valid():
            form.save()
    return render(request, 'frontend/company_profile.html', {'companyprofile': company})
