from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Customer
from .resources import CustomerResource

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = ('name', 'phone', 'vehicle_type', 'license_plate', 'created_at', 'created_by', 'price', 'payment_day')
    list_filter = ('vehicle_type', 'payment_day')
    search_fields = ('name', 'license_plate')
