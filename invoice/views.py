from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from customers.models import Customer
from .forms import InvoiceForm, MoreInfoForm, MoreInfoFormSet
from django.contrib import messages
from .models import Invoice, MoreInfo

# Create your views here.
def invoices(request):
    invoices = Invoice.objects.prefetch_related('moreinfo_set').order_by('-created_at')

    ctx = {
        'invoices': invoices,
        'title': "Facturas",
        }
    return render(request, 'invoices.html', ctx)

class InvoiceInline:
    form_class = InvoiceForm
    model = Invoice
    template_name = "invoice_create_update.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user 
        named_formsets = self.get_named_formsets()
        # form.instance.created_by = self.request.user 

    # Verificar si el formulario principal es válido
        if not form.is_valid():
            print(form.errors)  # Imprimir errores del formulario en la consola
            return self.render_to_response(self.get_context_data(form=form))

        if not all((x.is_valid() for x in named_formsets.values())):
            for name, formset in named_formsets.items():
                if not formset.is_valid():
                    print(f"Errores en el formset '{name}': {formset.errors}")
            return self.render_to_response(self.get_context_data(form=form))

        is_update = form.instance.pk is not None  # Verifica si es una actualización
        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func:
                formset_save_func(formset)
            else:
                # Asignar la factura guardada (self.object) a los objetos del formset antes de guardar
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.invoice = self.object  # Asignar la instancia principal
                    instance.save()
                formset.save_m2m()

        # Añadir mensaje dependiendo de si es creación o actualización
        if is_update:
            messages.success(self.request, 'Factura Actualizada.')
        else:
            messages.success(self.request, 'Factura Creada.')

        return redirect('invoice')
    
    def formset_invoices_data_valid(self, formset):
        invoices_data = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for invoice_data in invoices_data:
            invoice_data.invoice = self.object  # Asegurarse de que se asigne la factura guardada
            invoice_data.save()

class InvoiceCreate(InvoiceInline, CreateView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'invoice_data': MoreInfoFormSet(prefix='invoice_data'),
            }
        else:
            return {
                'invoice_data': MoreInfoFormSet(self.request.POST or None, instance=self.object, prefix='invoice_data'),
            }
        
class InvoiceUpdate(InvoiceInline, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'invoice_data': MoreInfoFormSet(instance=self.object, prefix='invoice_data'),
            }
        else:
            return {
                'invoice_data': MoreInfoFormSet(self.request.POST or None, instance=self.object, prefix='invoice_data'),
            }

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(
        html, dest=result
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result

def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    total_amount = sum(detail.total_price() for detail in invoice.moreinfo_set.all())
    context = {'invoice': invoice, 'total_amount': total_amount}
    return render_to_pdf('invoice_pdf_template.html', context)

def create_invoice_from_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)

    initial_data = {
        'parking_id': customer.parking_id,
        'customer_name': customer.name,
        'phone': customer.phone,
        'vehicle_type': customer.vehicle_type,
        'license_plate': customer.license_plate,
    }

    prefix = 'invoice_data'

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = MoreInfoFormSet(request.POST, prefix=prefix)

        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()

            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.invoice = invoice
                detalle.save()
            formset.save_m2m()

            messages.success(request, 'Factura creada correctamente.')
            return redirect('invoice')
    else:
        form = InvoiceForm(initial=initial_data)
        formset = MoreInfoFormSet(prefix=prefix)

    context = {
        'form': form,
        'named_formsets': {'invoice_data': formset},
    }

    return render(request, 'invoice_create_update.html', context)