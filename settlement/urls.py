from django.urls import path
from . import views


urlpatterns = [
    path('parqueadero-hoyo/', views.settlement_list, name='parking'),
    
    path('agregar-liquidacion/', views.CreateSettlementView.as_view(), name='add_parking'),
    path('agregar-lavado/', views.create_washing_ajax, name='create_washing_ajax'),
    
    #--------------------- update
    path('liquidacion/<int:pk>/editar/', views.SettlementUpdateView.as_view(), name='update_parking'),
    path('liquidacion/get-washing/<int:pk>/', views.get_washing, name='get_washing'),
    path('liquidacion/update-washing-ajax/', views.update_washing_ajax, name='update_washing_ajax'),
    
]