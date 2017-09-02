from __future__ import unicode_literals, absolute_import

from company.models import CompanyProfile
from client.models import ClientProfile
from django.db import transaction
from django.views.generic import CreateView, ListView
from .forms import InvoiceForm, ItemFormSet
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from customer.models import Bank, Tax
from .models import Invoice


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
        }
    }
    return JsonResponse(data)


def client_detail(request):
    client_id = request.GET['client_id']
    client_object = ClientProfile.objects.get(pk=client_id)

    data = {
        'results': {
                    'recipient': client_object.name,
                    "gst": client_object.gst,
                    "billing_address": client_object.billing_address.address
        }
    }
    return JsonResponse(data)


# def bill_list(request):
#     return HttpResponse('hello')


class InvoiceList(ListView):
    model = Invoice


class ItemCreate(CreateView):
    form_class = InvoiceForm
    template_name = 'frontend/bill_add.html'
    # success_url = reverse_lazy("bill_list")

    def get_context_data(self, **kwargs):
        data = super(ItemCreate, self).get_context_data(**kwargs)
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
        return super(ItemCreate, self).form_valid(form)

        # def get_success_url(self):
        #     return reverse('add_bill')
