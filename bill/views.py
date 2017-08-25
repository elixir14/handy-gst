from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def add_bill(request):
    return render(request, 'frontend/bill_add.html')
