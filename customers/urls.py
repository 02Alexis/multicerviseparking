from django.urls import path
from . import views


urlpatterns = [

    #--------------------- vista 
    path('parqueadero-hoyo/', views.customers_list, name='customer_list'),
    path('customers/paid/', views.customers_paid_list, name='customers_paid_list'),

    #--------------------- create
    path('nuevo-cliente', views.CustomerCreateView.as_view(), name='create_customer'),
    
    #--------------------- update
    path('cliente/<int:pk>/editar/', views.CustomerUpdateView.as_view(), name='update_customer'),

    path('reset_status/', views.reset_customers_status, name='reset_customers_status'),
    path('customers/mark-paid/', views.mark_customer_paid, name='mark_customer_paid'),
]