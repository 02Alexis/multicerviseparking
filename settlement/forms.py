# forms.py
from django import forms
from .models import *

class WashingForm(forms.ModelForm):
    class Meta:
        model = Washing
        fields = ['date', 'client_name', 'client_phone', 'vehicle_type', 'vehicle_plate', 'washing_price', 'worker', 'status']
        labels = {
            'date': 'Fecha',
            'client_name': 'Nombre del Cliente',
            'client_phone': 'Telefono del Cliente',
            'vehicle_type': 'Tipo de Vehiculo',
            'vehicle_plate': 'Placa del Vehiculo',
            'washing_price': 'Precio del Lavado',
            'worker': 'Trabajador',
            'status': 'Estado',
        }
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'washing_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'worker': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worker'].queryset = Worker.objects.filter(role__name='LAVADOR')

class SettlementForm(forms.ModelForm):
    class Meta:
        model = Settlement
        fields = ['parking_id', 'date', 'washing', 'total_amount', 'percentage', 'final_amount', 'parking_revenue', 'image']
        labels = {
            'parking_id': 'Parqueadero',
            'date': 'Fecha',
            'washing': 'Lavados',
            'total_amount': 'Monto Total',
            'percentage': 'Porcentaje',
            'final_amount': 'Monto Final',
            'image': 'Imagen',
            'parking_revenue': 'Total Parqueadero',
        }
        widgets = {
            'parking_id': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'washing': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'final_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'parking_revenue': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Mostrar lavados ya seleccionados + lavados no asociados a ninguna liquidación
            self.fields['washing'].queryset = Washing.objects.filter(
                models.Q(settlement__isnull=True) | models.Q(settlement=self.instance)
            ).distinct()
        else:
            self.fields['washing'].queryset = Washing.objects.filter(settlement__isnull=True)

