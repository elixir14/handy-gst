from __future__ import unicode_literals, absolute_import

from company.models import CompanyProfile
from client.models import ClientProfile
from django.db import transaction
from django.views.generic import CreateView, UpdateView
from .forms import InvoiceForm, ItemFormSet
from django.http import JsonResponse, HttpResponse
from customer.models import Bank, Tax, Address, State, Contact
from .models import Invoice, Item
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
# from weasyprint import HTML, CSS
from django.conf import settings
from num2words import num2words


@login_required
def generate_pdf(request, id=None):
    if id:
        invoice_object = get_object_or_404(Invoice, pk=id)
        item_object = Item.objects.filter(invoice_id=invoice_object.id)
        company_object = CompanyProfile.objects.get(pk=invoice_object.company_id)
        client_object = ClientProfile.objects.get(pk=invoice_object.client_id)
        bank_object = Bank.objects.get(id=company_object.bank_detail_id)
        tax_object = Tax.objects.get(id=company_object.tax_detail_id)
        address_object = Address.objects.get(pk=company_object.address_id)
        state_object = State.objects.get(id=address_object.state_id)
        contact_object = Contact.objects.get(pk=company_object.contact_id)
        total = {'quantity': 0, 'rate': 0, 'value': 0, 'discount': 0, 'tax_value': 0}
        for item in item_object:
            total['quantity'] += item.quantity
            total['rate'] += item.rate
            total['value'] += item.value
            total['discount'] += item.discount
            total['tax_value'] += item.tax_value
        data = {'invoice': invoice_object,
                'company': company_object,
                'client': client_object,
                'company_address': address_object,
                'company_state': state_object,
                'bank_detail': bank_object,
                'tax_detail': tax_object,
                'contact_detail': contact_object,
                'items': item_object,
                'total': total,
                'total_in_words': num2words(invoice_object.grand_total, lang='en').capitalize(),
                'title': invoice_object.invoice_no
        }
        # Rendered
        # html_string = render_to_string('frontend/gst_bill.html', context=data)
        html_string = render_to_string('frontend/bill.html', context=data)
        # html = HTML(string=html_string)
        pdf_file = html.write_pdf()
        # pdf_file = html.write_pdf(stylesheets=[CSS(settings.STATIC_ROOT + '//frontend//css//gst_bill_style.css')])

        # Creating http response
        response = HttpResponse(pdf_file, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=%s.pdf' % invoice_object.invoice_no
        return response
    else:
        return HttpResponse("No Invoice")


@login_required
def company_detail(request):
    result = {
            "remarks": "",
            "terms": "",
            "authorised_signatory": "",
            "account_number": "",
            "ifsc": "",
            "pan": "",
            "clients": [],
            "cgst": 0.00,
            "sgst": 0.00,
            "igst": 0.00
        }
    try:
        company_id = request.GET['id_company']
        company_object = CompanyProfile.objects.get(pk=company_id)
        result["remarks"] = company_object.remarks
        result["terms"] = company_object.terms
        result["authorised_signatory"] = company_object.authorised_signatory

        clients = []
        client_object = ClientProfile.objects.filter(company_id=company_object.id)
        for client in client_object:
            clients.append(dict(id=client.id, value=client.client_name))
        result["clients"] = clients

        bank_detail = company_object.bank_detail if company_object.bank_detail else None
        tax_detail = company_object.tax_detail if company_object.tax_detail else None

        result["account_number"] = bank_detail.account_number if bank_detail else ""
        result["ifsc"] = bank_detail.ifsc if bank_detail else ""
        result["pan"] = tax_detail.pan if tax_detail else ""

        result["cgst"] = tax_detail.cgst if tax_detail else 0.00
        result["sgst"] = tax_detail.sgst if tax_detail else 0.00
        result["igst"] = tax_detail.igst if tax_detail else 0.00
    except:
        pass

    data = {
        'results': result
    }
    return JsonResponse(data)

@login_required
def client_detail(request):
    result = {
                "recipient": "",
                "gst": "",
                "billing_address": "",
                "billing_state": "",
                "billing_state_code": "",
                "shipping_address": "",
                "shipping_state": "",
                "shipping_state_code": ""
    }
    try:
        client_id = request.GET['id_client']
        client_object = ClientProfile.objects.get(pk=client_id)
        result["recipient"] = client_object.client_name
        result["gst"] = client_object.gst
        try:
            billing_address_object = Address.objects.get(pk=client_object.billing_address_id)
            billing_state_object = billing_address_object.state
            result["billing_address"] = billing_address_object.address
            result["billing_state"] = billing_state_object.name if billing_state_object else ""
            result["billing_state_code"] = billing_state_object.code if billing_state_object else ""
        except Address.DoesNotExist:
            pass

        try:
            shipping_address_object = Address.objects.get(pk=client_object.shipping_address_id)
            shipping_state_object = shipping_address_object.state
            result["shipping_address"] = shipping_address_object.address
            result["shipping_state"] = shipping_state_object.name if shipping_state_object else ""
            result["shipping_state_code"] = shipping_state_object.code if shipping_state_object else ""
        except Address.DoesNotExist:
            pass
    except Exception, ex:
        pass
    data = {
        'results': result
    }
    return JsonResponse(data)


@login_required
def bill_list(request, id=None):
    invoices = Invoice.objects.all()
    # for invoice in invoices:
    #     company = CompanyProfile.objects.get(pk=invoice.company_id)
    #     invoice.company_id = company.company_name
    data = {'clients': invoices}
    return render(request, "frontend/invoice_list.html", context=data)


class ItemCreate(CreateView):
    form_class = InvoiceForm
    model = Invoice
    template_name = 'frontend/invoice_form.html'
    success_url = reverse_lazy("frontend:bill:bill_list")

    def __init__(self, **kwargs):
        self.object = None
        super(ItemCreate, self).__init__(**kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super(ItemCreate, self).get_form_kwargs()
    #     return kwargs

    def get_context_data(self, **kwargs):
        data = super(ItemCreate, self).get_context_data(user=self.request.user, **kwargs)
        print self.request.POST

        if self.request.POST:
            data['items'] = ItemFormSet(self.request.POST)
        else:
            data['items'] = ItemFormSet()
        return data

    def form_valid(self, form):
        print '0000000000000000000000000000'
        context = self.get_context_data()
        print '1111111111111111111111111'
        items = context['items']
        print items
        if not form.is_valid():
            print 'kkkkkkkkkkkkkkkkkkkkkkkkkkkkk'
            print form.errors
        with transaction.atomic():
            self.object = form.save()
            if items.is_valid():
                items.instance = self.object
                items.save()
            else:
                print items.errors
        return super(ItemCreate, self).form_valid(form)


class ItemUpdate(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = "frontend/invoice_form.html"
    success_url = reverse_lazy("frontend:bill:bill_list")

    def __init__(self, **kwargs):
        self.object = None
        super(ItemUpdate, self).__init__(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(ItemUpdate, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

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
        return super(ItemUpdate, self).form_valid(form)


@login_required
def bill_delete(request, id):
    # invoice = Invoice.objects.for_user(user=request.user).get(pk=id)
    invoices = Invoice.objects.filter(company__customer__user=request.user)
    for invoice in invoices:
        if str(invoice.id) == id:
            invoice.delete()
    # invoices = Invoice.objects.for_user(user=request.user)
    invoices = Invoice.objects.filter(company__customer__user=request.user)
    return render(request, "frontend/invoice_list.html", {'clients': invoices})
