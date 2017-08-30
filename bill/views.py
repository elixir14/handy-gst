from __future__ import unicode_literals, absolute_import

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from company.models import CompanyProfile
from client.models import ClientProfile
from customer.models import CustomerProfile
from .models import Invoice, Item
from django.urls import reverse

from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView
from .forms import InvoiceForm, ItemFormSet

# @login_required
# def add_bill(request):
#     companies = CompanyProfile.objects.all().order_by('name')
#     clients = ClientProfile.objects.all().order_by('name')
#     form = ItemFormSet()
#     # if request.method == "POST":
#     #     print (request.POST)
#
#     return render(request, 'frontend/bill_add.html', {'form': form, 'companies': companies, 'client': clients})


# class InvoiceCreate(CreateView):
#     model = Invoice
#     fields = ['invoice_no', 'invoice_date', 'gst', '']

class ItemCreate(CreateView):
    form_class = InvoiceForm
    template_name = 'frontend/bill_add.html'

    def get_context_data(self, **kwargs):
        data = super(ItemCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = ItemFormSet(self.request.POST)
        else:
            data['items'] = ItemFormSet()
        data['companies'] = CompanyProfile.objects.all()
        data['clients'] = ClientProfile.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
        return super(ItemCreate, self).form_valid(form)

    # def get_success_url(self):
    #     return reverse('add_bill')