from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from parking.models import Parking, Vehicle_Type

class Invoice(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('CEDULA', 'Cédula'),
        ('NIT', 'NIT'),
    ]
    
    parking_id = models.ForeignKey(Parking, null=False, blank=False, on_delete=models.RESTRICT)
    date = models.DateField(default=timezone.localdate)  # Fecha de emisión de la factura
    customer_name = models.CharField(max_length=100)  # Nombre del cliente
    phone = models.CharField(max_length=15)  # Teléfono del cliente
    vehicle_type = models.ForeignKey(Vehicle_Type, null=True, blank=True, on_delete=models.RESTRICT)
    license_plate = models.CharField(max_length=10, blank=True, null=True)  # Placa del vehículo (opcional si no es cliente)
    address = models.CharField(max_length=255, blank=True, null=True)  # Dirección del cliente (opcional si no es cliente)
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES, blank=True, null=True)  # Tipo de documento (opcional)
    number = models.CharField(max_length=20, blank=True, null=True)  # Número de cédula o NIT (opcional)
    email = models.EmailField()  # Correo electrónico del cliente para enviar la factura
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Usuario que creó la factura

    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoice_modified')

    def __str__(self):
        return f"Factura {self.id} - {self.customer_name} - {self.vehicle_type}"
    
    @property
    def modified_by_name(self):
        if self.modified_by:
            return self.modified_by.get_full_name() or self.modified_by.username
        return "Desconocido"
    
class MoreInfo(models.Model):
    PRODUCT_CHOICES = [
        ('PARKING_OCCASIONAL', 'Parqueo Ocasional'),
        ('MONTHLY_PAYMENT', 'Mensualidad'),
        ('WASH', 'Lavado'),
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.CharField(max_length=20, choices=PRODUCT_CHOICES)  # Producto
    quantity = models.PositiveIntegerField()  # Cantidad de productos
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Precio

    def total_price(self):
        return self.quantity * self.price  # Multiplica cantidad por precio unitario

    def __str__(self):
        return f"{self.product} - {self.quantity} x {self.price}"

