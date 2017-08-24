from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .forms import EditCustomerForm


@login_required
def customer_profile(request):
    user = request.user
    return render(request, 'frontend/customer_profile.html', {'user': user})


@login_required
def edit_customer_profile(request, id=None):
    if id:
        user = get_object_or_404(User, pk=id)
        form = EditCustomerForm(request.POST or None, instance=user)
        if request.POST and form.is_valid():
            form.save()
    return render(request, 'frontend/customer_profile.html', {'user': user})
