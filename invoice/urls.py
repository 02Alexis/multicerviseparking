from django.urls import path
from . import views


urlpatterns = [
    path('facturas/', views.invoices, name='invoice'),
    path('nueva-factura', views.InvoiceCreate.as_view(), name='create_invoice'),
    path('factura/<int:pk>/editar/', views.InvoiceUpdate.as_view(), name='update_invoice'),
    path('factura/<int:pk>/pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('invoice/create_from_customer/<int:customer_id>/', views.create_invoice_from_customer, name='create_invoice_from_customer'),
]