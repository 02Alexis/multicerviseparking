from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from parking.models import Parking, Vehicle_Type, Worker
from cloudinary.models import CloudinaryField

# Función para rutas dinámicas
def get_upload_path(instance, filename):
    """
    Genera: 'settlements/[id_parqueadero]-[nombre-slug]/[filename]'
    Ejemplo: 'settlements/5-parqueadero-centro/foto.jpg'
    """
    parking = instance.parking_id
    return f'settlements/{parking.id}-{slugify(parking.name)}/{filename}'

# Create your models here.
class Washing(models.Model):
    date = models.DateField(default=timezone.localdate)
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20, null=True, blank=True)
    vehicle_type = models.ForeignKey(Vehicle_Type, null=True, blank=True, on_delete=models.RESTRICT)
    vehicle_plate = models.CharField(max_length=20)
    washing_price = models.DecimalField(max_digits=10, decimal_places=2)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pagado', 'Pagado'),
        ('no_pagado', 'No Pagado'),
        ('arm', 'ARM'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Lavado de {self.client_name} - {self.vehicle_type} - {self.vehicle_plate}"

class Settlement(models.Model):
    parking_id = models.ForeignKey(Parking, null=False, blank=False, on_delete=models.RESTRICT)
    date = models.DateField(default=timezone.localdate)
    washing = models.ManyToManyField('Washing', blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image = CloudinaryField('image', blank=True, null=True)
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=35.00,
        verbose_name='Trabajadores (%)'
    )
    final_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name='Monto final'
    )
    parking_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Total'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Usuario que creó el registro

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='settlement_modified')

    class Meta:
        ordering = ['-created_at']

    @property
    def calculated_percentage(self):
        """Muestra el monto del porcentaje como valor absoluto"""
        return self.total_amount * (self.percentage / 100)

    @property
    def total_with_parking(self):
        """Suma final_amount con parking_revenue"""
        return self.final_amount + self.parking_revenue

    def __str__(self):
        return (f"Liquidación del {self.date} - Total: ${self.total_amount} - "
                f"{self.percentage}%: ${self.calculated_percentage:.2f} - "
                f"Final: ${self.final_amount} - "
                f"Total con Parqueo: ${self.total_with_parking}")

    def calculate_amounts(self):
        """
        Nueva lógica:
        1. Suma TODOS los lavados (pagados + arm + no_pagados)
        2. Aplica el porcentaje al total
        3. Resta los lavados 'arm' y 'no_pagado' del monto descontado
        """
        total_todos = 0
        total_deudas = 0  # Suma de arm + no_pagado
        
        for washing in self.washing.all():
            if washing.status == 'cancelado':
            # Tratar cancelado igual que arm/no_pagado
                total_todos += washing.washing_price
                total_deudas += washing.washing_price
            elif washing.status != 'cancelado':  # Excluir solo cancelados reales
                total_todos += washing.washing_price
                if washing.status in ['arm', 'no_pagado']:
                    total_deudas += washing.washing_price
        
        self.total_amount = total_todos
        monto_descontado = total_todos * (self.percentage / 100)
        self.final_amount = (total_todos - monto_descontado) - total_deudas
        
        self.save(update_fields=['total_amount', 'final_amount'])

    def payments_per_worker(self):
        """
        Retorna un diccionario con el trabajador como clave y el monto a pagar como valor,
        calculado aplicando el porcentaje al total de lavados de cada trabajador.
        """
        # Diccionario para acumular total por trabajador
        worker_totals = {}

        # Sumar los precios de lavados por trabajador
        for washing in self.washing.all():
            worker = washing.worker
            if worker not in worker_totals:
                worker_totals[worker] = 0
            worker_totals[worker] += washing.washing_price

        # Calcular el pago proporcional según el porcentaje
        payments = {}
        for worker, total in worker_totals.items():
            payments[worker] = total * (self.percentage / 100)

        return payments

    @property
    def modified_by_name(self):
        if self.modified_by:
            return self.modified_by.get_full_name() or self.modified_by.username
        return "Desconocido"