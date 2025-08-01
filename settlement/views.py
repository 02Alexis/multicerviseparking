from django.shortcuts import render, redirect, get_object_or_404
from collections import defaultdict
from django.utils import timezone
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from parking.models import UserParkingAssignment

# Create your views here.
# --------- vistas
@login_required(login_url='login')
def home(request):
    return render(request, '404.html')

@login_required(login_url='login')
def settlement_list(request):
    user = request.user
    parkings = Parking.objects.all()

    parking_id = None  # Inicializar para evitar UnboundLocalError

    # Determinar parqueadero asignado (si existe)
    assigned_parking = None
    if not user.is_superuser and not user.is_staff:
        try:
            assigned_parking = user.assigned_parking.parking
        except UserParkingAssignment.DoesNotExist:
            assigned_parking = None

    # Filtrar liquidaciones según rol y asignación
    if user.is_superuser or user.is_staff:
        settlements = Settlement.objects.all().select_related('parking_id').prefetch_related('washing').order_by('-created_at')
        parking_id = request.GET.get('parking_id')
        if parking_id:
            settlements = settlements.filter(parking_id__id=parking_id).order_by('-created_at')
    else:
        if assigned_parking is None:
            settlements = Settlement.objects.none()
        else:
            settlements = Settlement.objects.filter(parking_id=assigned_parking).select_related('parking_id').prefetch_related('washing').order_by('-created_at')
            parking_id = assigned_parking.id

    ctx = {
        'settlements': settlements,
        'title': "Liquidaciones",
        'label': "Liquidaciones",
        'parkings': parkings if (user.is_superuser or user.is_staff) else [assigned_parking] if assigned_parking else [],
        'selected_parking_id': int(parking_id) if parking_id else None,
        'assigned_parking': assigned_parking,
    }
    return render(request, 'settlement_list.html', ctx)

# --------- funcion para crear
class CreateSettlementView(CreateView):
    template_name = 'form/create_settlement.html'
    model = Settlement
    form_class = SettlementForm

    def form_valid(self, form):
        settlement = form.save(commit=False)
        settlement.created_by = self.request.user
        settlement.modified_by = self.request.user

        # Forzar parking_id según usuario asignado
        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            try:
                assigned_parking = user.assigned_parking.parking
                settlement.parking_id = assigned_parking
            except UserParkingAssignment.DoesNotExist:
                messages.error(self.request, "No tienes un parqueadero asignado. Contacta al administrador.")
                return self.form_invalid(form)
        # Si es admin, puede elegir el parking normalmente

        settlement.save()
        form.save_m2m()
        settlement.calculate_amounts()
        messages.success(self.request, "Liquidación creada exitosamente.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("Errores de formulario:", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settlement'] = self.object
        context['title'] = 'Agregar Liquidación'
        context['label'] = 'Crear'
        context['washing_form'] = WashingForm()
        return context

    def get_success_url(self):
        return reverse('parking')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if not user.is_superuser and not user.is_staff:
            try:
                assigned_parking = user.assigned_parking.parking
                form.fields['parking_id'].queryset = Parking.objects.filter(id=assigned_parking.id)
                form.fields['parking_id'].initial = assigned_parking
                form.fields['parking_id'].disabled = True  # Deshabilita el campo visualmente
            except UserParkingAssignment.DoesNotExist:
                form.fields['parking_id'].queryset = Parking.objects.none()
        return form
        
@csrf_exempt
def create_washing_ajax(request):
    if request.method == 'POST':
        form = WashingForm(request.POST)
        if form.is_valid():
            washing = form.save()
            settlement_id = request.POST.get('settlement_id')
            if settlement_id:
                settlement = Settlement.objects.get(pk=settlement_id)
                settlement.washing.add(washing)
            return JsonResponse({
                'id': washing.id,
                'text': str(washing)
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)

# --------- funcion para actualizar
class SettlementUpdateView(UpdateView):
    model = Settlement
    form_class = SettlementForm
    template_name = 'form/update_settlement.html'

    def form_valid(self, form):
        settlement = form.save(commit=False)
        settlement.modified_by = self.request.user
        settlement.save()
        form.save_m2m()
        settlement.calculate_amounts()
        messages.success(self.request, "Liquidación actualizada exitosamente.")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la liquidación.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settlement'] = self.object
        context['title'] = 'Actualizar Liquidación'
        context['label'] = 'Actualizar'
        context['washing_form'] = WashingForm()
        return context

    def get_success_url(self):
        return reverse('parking')

@csrf_exempt
def update_washing_ajax(request):
    if request.method == 'POST':
        washing_id = request.POST.get('washing_id')
        washing = get_object_or_404(Washing, pk=washing_id)
        form = WashingForm(request.POST, instance=washing)
        if form.is_valid():
            washing = form.save()
            return JsonResponse({
                'id': washing.id,
                'text': str(washing)
            })
        else:
            return JsonResponse({'errors': form.errors}, status=400)

def get_washing(request, pk):
    washing = get_object_or_404(Washing, pk=pk)
    data = {
        'id': washing.id,
        'date': washing.date.strftime('%Y-%m-%d'),
        'client_name': washing.client_name,
        'client_phone': washing.client_phone,
        'vehicle_type': washing.vehicle_type_id,  # ID del ForeignKey
        'vehicle_plate': washing.vehicle_plate,
        'washing_price': str(washing.washing_price),
        'worker': washing.worker_id,  # ID del ForeignKey
        'status': washing.status,
    }
    return JsonResponse(data)
    
@login_required(login_url='login')
def settlement_chart_view(request):
    from collections import defaultdict
    import datetime
    parkings = Parking.objects.all()
    selected_parking_id = request.GET.get('parking_id')
    year = request.GET.get('year')
    month = request.GET.get('month')

    today = timezone.localdate()
    if not year:
        year = today.year
    else:
        year = int(year)
    if not month:
        month = today.month
    else:
        month = int(month)

    settlements = Settlement.objects.filter(date__year=year, date__month=month)
    if selected_parking_id:
        settlements = settlements.filter(parking_id_id=selected_parking_id)

    totals_by_parking = defaultdict(float)
    for settlement in settlements:
        parking_name = settlement.parking_id.name
        totals_by_parking[parking_name] += float(settlement.total_with_parking)

    labels = list(totals_by_parking.keys())
    totals = list(totals_by_parking.values())

    # Lista de años (últimos 10 años)
    current_year = today.year
    years = list(range(current_year - 9, current_year + 1))

    # Lista de meses 1-12
    months = list(range(1, 13))

    context = {
        'parkings': parkings,
        'data': {
            'labels': labels,
            'totals': totals,
        },
        'selected_parking_id': int(selected_parking_id) if selected_parking_id else None,
        'selected_year': year,
        'selected_month': month,
        'years': years,
        'months': months,
    }
    return render(request, 'settlement_chart.html', context)
