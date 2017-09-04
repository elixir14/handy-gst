from __future__ import unicode_literals, absolute_import

from company.models import CompanyProfile
from client.models import ClientProfile
from django.db import transaction
from django.views.generic import CreateView, ListView, UpdateView
from .forms import InvoiceForm, ItemFormSet
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from customer.models import Bank, Tax, Address
from .models import Invoice
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy


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

def company_detail(request):
    company_id = request.GET['company_id']
    # print (company_id)
    company_object = CompanyProfile.objects.get(pk=company_id)
    clients = []
    client_object = ClientProfile.objects.filter(company_id=company_object.id)
    for client in client_object:
        clients.append(dict(id=client.id, value=client.name))

    bank_detail = Bank.objects.get(id=company_object.bank_detail_id)
    tax_detail = Tax.objects.get(id=company_object.tax_detail_id)

    data = {
        'results': {
            "remarks": company_object.remarks,
            "terms": company_object.terms,
            "authorised_signatory": company_object.authorised_signatory,
            "account_number": bank_detail.name,
            "ifsc": bank_detail.ifsc,
            "pan": tax_detail.pan,
            "clients": clients,
            "cgst": tax_detail.cgst,
            "sgst": tax_detail.sgst,
            "igst": tax_detail.igst,
        }
    }
    return JsonResponse(data)


def client_detail(request):
    client_id = request.GET['client_id']
    client_object = ClientProfile.objects.get(pk=client_id)
    # print(client_object.__dict__)

    # address_object = Address.objects.get(pk=client_object.billing_address_id)


    data = {
        'results': {
                    "recipient": client_object.name,
                    "gst": client_object.gst,
                    "billing_address": 'Palanpur'#address_object.value
        }
    }
    return JsonResponse(data)


def bill_list(request, id=None):
    if id:
        invoice = Invoice.objects.get(pk=id)
    else:
        invoice = Invoice.objects.all()
    return render(request, "frontend/invoice_list.html", {'clients': invoice})


class InvoiceList(ListView):
    model = Invoice


class ItemCreate(CreateView):
    form_class = InvoiceForm
    template_name = 'frontend/invoice_form.html'
    # success_url = reverse_lazy("bill_list")

    def __init__(self, **kwargs):
        super(ItemCreate, self).__init__(**kwargs)
        self.request = None
        self.object = None

    def get_context_data(self, **kwargs):
        data = super(ItemCreate, self).get_context_data(**kwargs)
        print (self.request.POST)
        if self.request.POST:
            data['items'] = ItemFormSet(self.request.POST)
        else:
            data['items'] = ItemFormSet()
        return data

    def form_valid(self, form):
        print (self.request.POST)
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                print ("inside  save")
                items.instance = self.object
                items.save()
                print ("save done")
            else:
                print ("-------Error-----")
        return super(ItemCreate, self).form_valid(form)

        # def get_success_url(self):
        #     return reverse('add_bill')


class ItemUpdate(UpdateView):
    model = Invoice
    fields = "__all__"
    template_name = "frontend/invoice_form.html"
    success_url = reverse_lazy('bill_list')

    def __init__(self, **kwargs):
        super(ItemUpdate, self).__init__(**kwargs)
        self.request = None
        self.object = None

    def get_context_data(self, **kwargs):
        data = super(ItemUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = ItemFormSet(self.request.POST, instance=self.object)
        else:
            data['items'] = ItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
            else:
                print "error"
        return super(ItemUpdate, self).form_valid(form)