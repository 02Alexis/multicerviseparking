from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from .models import Settlement, Washing

class SettlementResource(resources.ModelResource):
    washing = fields.Field(
        column_name='washing',
        attribute='washing',
        widget=ManyToManyWidget(Washing, field='id')  # o usa otro campo único, como 'client_name' si prefieres
    )

    class Meta:
        model = Settlement
        fields = ('id', 'date', 'total_amount', 'percentage', 'calculated_percentage', 'final_amount', 'total_with_parking', 'washing')
        export_order = fields

class WashingResource(resources.ModelResource):
    class Meta:
        model = Washing
