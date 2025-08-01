from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import *
from .models import *

# Create your views here.

# --------- vistas
@login_required(login_url='login')
def customers_list(request):
    user = request.user
    parkings = Parking.objects.all()
    parking_id = None

    # Intentar obtener parqueadero asignado
    assigned_parking = None
    if not user.is_superuser and not user.is_staff:
        try:
            assigned_parking = user.assigned_parking.parking
        except UserParkingAssignment.DoesNotExist:
            assigned_parking = None

    if user.is_superuser or user.is_staff:
        customers = Customer.objects.filter(status='no_pagado')
        parking_id = request.GET.get('parking_id')
        if parking_id:
            customers = customers.filter(parking_id__id=parking_id)
    else:
        if assigned_parking is None:
            customers = Customer.objects.none()
        else:
            customers = Customer.objects.filter(parking_id=assigned_parking, status='no_pagado')
            parking_id = assigned_parking.id

    total_customers = customers.count()
    no_pagado_count = customers.filter(status='no_pagado').count()
    can_reset = total_customers != no_pagado_count

    ctx = {
        'customers': customers,
        'can_reset': can_reset,
        'title': "Mensualidades",
        'parkings': parkings if (user.is_superuser or user.is_staff) else [assigned_parking] if assigned_parking else [],
        'selected_parking_id': int(parking_id) if parking_id else None,
        'assigned_parking': assigned_parking,
    }
    return render(request, 'index/customer_list.html', ctx)

@login_required(login_url='login')
def customers_paid_list(request):
    user = request.user
    parkings = Parking.objects.all()
    parking_id = None

    assigned_parking = None
    if not user.is_superuser and not user.is_staff:
        try:
            assigned_parking = user.assigned_parking.parking
        except UserParkingAssignment.DoesNotExist:
            assigned_parking = None

    if user.is_superuser or user.is_staff:
        customers = Customer.objects.filter(status='pagado')
        parking_id = request.GET.get('parking_id')
        if parking_id:
            customers = customers.filter(parking_id__id=parking_id)
    else:
        if assigned_parking is None:
            customers = Customer.objects.none()
        else:
            customers = Customer.objects.filter(parking_id=assigned_parking, status='pagado')
            parking_id = assigned_parking.id

    total_customers = customers.count()
    no_pagado_count = customers.filter(status='no_pagado').count()
    can_reset = total_customers != no_pagado_count

    ctx = {
        'customers': customers,
        'can_reset': can_reset,
        'title': "Clientes Pagados",
        'parkings': parkings if (user.is_superuser or user.is_staff) else [assigned_parking] if assigned_parking else [],
        'selected_parking_id': int(parking_id) if parking_id else None,
        'assigned_parking': assigned_parking,
    }
    return render(request, 'index/customer_list.html', ctx)

# --------- funcion para crear
class CustomerCreateView(CreateView):
    template_name = 'form/create_customer_modal.html'
    model = Customer
    form_class = CustomerForm

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.created_by = self.request.user  # Asigna el usuario que crea

        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            try:
                assigned_parking = user.assigned_parking.parking
                customer.parking_id = assigned_parking
            except UserParkingAssignment.DoesNotExist:
                messages.error(self.request, "No tienes un parqueadero asignado. Contacta al administrador.")
                return self.form_invalid(form)

        customer.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object
        context['title'] = 'Nuevo Cliente'
        context['label'] = 'Crear'
        return context

    def get_success_url(self):
        return reverse('customer_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            try:
                assigned_parking = user.assigned_parking.parking
                form.fields['parking_id'].queryset = Parking.objects.filter(id=assigned_parking.id)
                form.fields['parking_id'].initial = assigned_parking
                form.fields['parking_id'].disabled = True  # Opcional: deshabilita para evitar cambios
            except UserParkingAssignment.DoesNotExist:
                form.fields['parking_id'].queryset = Parking.objects.none()
        return form
    
# --------- funcion para actualizar
class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'form/update_customer_modal.html'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.modified_by = self.request.user  # Asigna el usuario que modifica
        customer.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object
        context['title'] = 'Actualizar Cliente'
        context['label'] = 'Actualizar'
        return context

    def get_success_url(self):
        return reverse('customer_list')

@login_required
def reset_customers_status(request):
    total_customers = Customer.objects.count()

    if total_customers == 0:
        messages.info(request, "No hay clientes registrados para actualizar.")
        return redirect('customer_list')

    # Verificar si todos están ya en 'no_pagado'
    no_pagado_count = Customer.objects.filter(status='no_pagado').count()

    if total_customers == no_pagado_count:
        # Todos ya están en 'no_pagado', no hacer nada
        messages.info(request, "Todos los clientes ya están en estado 'No Pagado'. No es necesario reiniciar.")
    else:
        # Actualizar todos a 'no_pagado'
        updated_count = Customer.objects.update(status='no_pagado')
        messages.success(request, f'Se actualizaron {updated_count} clientes a "No Pagado".')

    return redirect('customer_list')

@login_required
@require_POST
def mark_customer_paid(request):
    customer_id = request.POST.get('customer_id')
    if not customer_id:
        return JsonResponse({'error': 'No se proporcionó el ID del cliente.'}, status=400)
    try:
        customer = Customer.objects.get(pk=customer_id)
        customer.status = 'pagado'
        customer.modified_by = request.user
        customer.save()
        return JsonResponse({'success': True, 'status': customer.status})
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado.'}, status=404)