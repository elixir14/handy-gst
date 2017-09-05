from __future__ import unicode_literals, absolute_import

from company.models import CompanyProfile
from client.models import ClientProfile
from django.db import transaction
from django.views.generic import CreateView, UpdateView
from .forms import InvoiceForm, ItemFormSet
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from customer.models import Bank, Tax, Address, State, Contact
from .models import Invoice, Item
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings


@login_required
def generate_pdf(request, id=None):
    if id:
        invoice_object = get_object_or_404(Invoice, pk=id)
        item_object = Item.objects.filter(invoice_id=invoice_object.id)
        company_object = CompanyProfile.objects.get(pk=invoice_object.company_id)
        bank_object = Bank.objects.get(id=company_object.bank_detail_id)
        tax_object = Tax.objects.get(id=company_object.tax_detail_id)
        address_object = Address.objects.get(pk=company_object.address_id)
        state_object = State.objects.get(id=address_object.state_id)
        contact_object = Contact.objects.get(pk=company_object.contact_id)
        data = {'invoice': invoice_object,
                'company': company_object,
                'company_address': address_object,
                'company_state': state_object,
                'bank_detail': bank_object,
                'tax_detail': tax_object,
                'contact_detail': contact_object,
                'items': item_object
        }
        # Rendered
        html_string = render_to_string('frontend/gst_bill.html', context=data)
        html = HTML(string=html_string)
        pdf_file = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '\\frontend\\css\\gst_bill_style.css')])

        # Creating http response
        response = HttpResponse(pdf_file, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=invoice.pdf'
        return response
    else:
        return HttpResponse("No Invoice")


def company_detail(request):
    company_id = request.GET['id_company']
    company_object = CompanyProfile.objects.get(pk=company_id)
    clients = []
    client_object = ClientProfile.objects.filter(company_id=company_object.id)
    for client in client_object:
        clients.append(dict(id=client.id, value=client.client_name))
    bank_detail = Bank.objects.get(id=company_object.bank_detail_id)
    tax_detail = Tax.objects.get(id=company_object.tax_detail_id)
    data = {
        'results': {
            "remarks": company_object.remarks,
            "terms": company_object.terms,
            "authorised_signatory": company_object.authorised_signatory,
            "account_number": bank_detail.account_number,
            "ifsc": bank_detail.ifsc,
            "pan": tax_detail.pan,
            "clients": clients,
            "cgst": tax_detail.cgst,
            "sgst": tax_detail.sgst,
            "igst": tax_detail.igst
        }
    }
    return JsonResponse(data)


def client_detail(request):
    client_id = request.GET['client_id']
    client_object = ClientProfile.objects.get(pk=client_id)
    billing_address_object = Address.objects.get(pk=client_object.billing_address_id)
    shipping_address_object = Address.objects.get(pk=client_object.shipping_address_id)
    billing_state_object = State.objects.get(pk=billing_address_object.state_id)
    shipping_state_object = State.objects.get(pk=shipping_address_object.state_id)
    data = {
        'results': {
            'recipient': client_object.client_name,
            "gst": client_object.gst,
            "billing_address": billing_address_object.address,
            "billing_state": billing_state_object.name,
            "billing_state_code": billing_state_object.code,
            "shipping_address": shipping_address_object.address,
            "shipping_state": shipping_state_object.name,
            "shipping_state_code": shipping_state_object.code,
        }
    }
    return JsonResponse(data)


def bill_list(request, id=None):
    if id:
        invoice = Invoice.objects.get(pk=id)
    else:
        invoice = Invoice.objects.all()
    return render(request, "frontend/invoice_list.html", {'clients': invoice})


class ItemCreate(CreateView):
    form_class = InvoiceForm
    model = Invoice
    template_name = 'frontend/invoice_form.html'
    success_url = reverse_lazy("frontend:bill:bill_list")

    def __init__(self, **kwargs):
        super(ItemCreate, self).__init__(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(ItemCreate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super(ItemCreate, self).get_context_data(user=self.request.user, **kwargs)
        if self.request.POST:
            data['items'] = ItemFormSet(self.request.POST)
        else:
            data['items'] = ItemFormSet()
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


class ItemUpdate(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "frontend/invoice_form.html"
    success_url = reverse_lazy("frontend:bill:bill_list")

    def __init__(self, **kwargs):
        super(ItemUpdate, self).__init__(**kwargs)

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
                print ("Error in saving form.")
        return super(ItemUpdate, self).form_valid(form)


def bill_delete(request, id=None):
    if id:
        invoice = Invoice.objects.get(pk=id)
        invoice.delete()
        invoices = Invoice.objects.all()
    return render(request, "frontend/invoice_list.html", {'clients': invoices})
