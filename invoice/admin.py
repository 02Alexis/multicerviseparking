from django.contrib import admin
from .models import Invoice, MoreInfo


class MoreInfoInline(admin.TabularInline):
    model = MoreInfo

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'customer_name',
        'phone',
        'vehicle_type',
        'license_plate',
        'address',
        'document_type',
        'number',
        'email',
        'created_by',
    )
    search_fields = (
        'customer_name',
        'phone',
        'vehicle_type',
        'license_plate',
        'address',
        'document_type',
        'number',
        'email',
        'created_by__username',
    )
    list_filter = (
        'date',
        'vehicle_type',
        'document_type',
        'created_by',
    )
    ordering = ('-date',)
    inlines = [
        MoreInfoInline,
    ]