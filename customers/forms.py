# forms.py
from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['parking_id', 'name', 'phone', 'vehicle_type', 'license_plate', 'price', 'payment_day', 'status']
        labels = {
            'parking_id': 'Establecimiento',
            'name' : 'Nombre',
            'phone': 'Telefono',
            'vehicle_type': 'Vehiculo',
            'license_plate' : 'Placa',
            'price' : 'Precio',
            'payment_day' : 'Día de Pago',
            'status' : 'Estado',
        }
        widgets = {
            'parking_id': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
