from django.db import models
from django.contrib.auth.models import User
from parking.models import Parking, Vehicle_Type

# Create your models here.
class Customer(models.Model):
    STATUS_CHOICES = [
        ('pagado', 'Pagado'),
        ('no_pagado', 'No Pagado'),
        ('congelado', 'Congelado'),
    ]
    parking_id = models.ForeignKey(Parking, null=False, blank=False, on_delete=models.RESTRICT)
    name = models.CharField(max_length=100)  # Nombre del cliente
    phone = models.CharField(max_length=15)  # Teléfono del cliente
    vehicle_type = models.ForeignKey(Vehicle_Type, null=True, blank=True, on_delete=models.RESTRICT)
    license_plate = models.CharField(max_length=10)  # Placa del vehículo
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Precio mensual
    payment_day = models.PositiveIntegerField()  # Día de pago (por ejemplo, 1, 15, 30)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='no_pagado')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Usuario que creó el registro

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers_modified')

    def __str__(self):  
        return f"{self.name} - {self.license_plate}"
    
    @property
    def formatted_license_plate(self):
        if len(self.license_plate) >=6:
            return f"{self.license_plate[:3]}-{self.license_plate[3:]}"
        return self.license_plate

    @property
    def modified_by_name(self):
        if self.modified_by:
            return self.modified_by.get_full_name() or self.modified_by.username
        return "Desconocido"

    def get_status_class(self):
        return {
            'pagado': 'table-success',
            'no_pagado': 'table-danger',
            'congelado': 'table-warning',
        }.get(self.status, '')