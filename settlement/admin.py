from django.contrib import admin

from .models import *
from django.db.models import Prefetch

# Register your models here.
@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_amount', 'percentage', 'calculated_percentage', 'final_amount', 'total_with_parking')
    date_hierarchy = 'date'
    search_fields = ('date',)
    filter_horizontal = ('washing',)
    readonly_fields = ('total_amount', 'calculated_percentage', 'final_amount', 'payments_per_worker_display', 'total_with_parking')
    list_select_related = ('parking_id',)

    # Opcional: Mostrar los lavados en la página de detalle
    def washings_list(self, obj):
        return ", ".join([str(w) for w in obj.washing.all()])
    washings_list.short_description = "Lavados incluidos"

    fieldsets = (
        (None, {
            'fields': ('parking_id', 'date', 'percentage', 'total_amount', 'calculated_percentage', 'final_amount', 'total_with_parking', 'washing')
        }),
    )

    def payments_per_worker_display(self, obj):
        pagos = obj.payments_per_worker()
        lines = [f"{worker}: ${monto:.2f}" for worker, monto in pagos.items()]
        return "<br>".join(lines)
    payments_per_worker_display.short_description = "Pago por trabajador"
    payments_per_worker_display.allow_tags = True

    # Agregar el método para mostrar el porcentaje calculado
    def calculated_percentage(self, obj):
        return f"${obj.calculated_percentage:.2f}"
    calculated_percentage.short_description = 'Monto del porcentaje'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            Prefetch('washing', queryset=Washing.objects.all())
        ).select_related('parking_id')
        
    def save_model(self, request, obj, form, change):
        # Primero guarda el objeto para generar el ID
        super().save_model(request, obj, form, change)
        
        # Actualizar relación many-to-many manualmente
        if 'washing' in form.cleaned_data:
            obj.washing.set(form.cleaned_data['washing'])
        
        # Recalcular el total CON los datos actualizados
        obj.calculate_amounts()
        
@admin.register(Washing)
class WashingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'client_name', 'client_phone', 'vehicle_type', 'vehicle_plate', 'washing_price', 'worker', 'status')
    search_fields = ('client_name', 'client_phone', 'vehicle_plate', 'status')
    list_filter = ('status', 'worker')