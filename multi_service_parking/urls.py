from django.contrib import admin
from django.urls import path
from django.urls import include
from settlement import views
from multi_service_parking import views as login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.settlement_chart_view, name='settlement_chart'),
    path('users/login', login.login_view, name='login'),
    path('users/logout', login.logout_view, name='logout'),
    path('register/', login.register_view, name='register'),
    path('account/', login.account, name='account'),
    path('liquidacion/', include('settlement.urls')), # Ruta para la página de inicio
    path('mensualidad/', include('customers.urls')), # Ruta para la página de inicio
    path('factura-electronica/', include('invoice.urls')), # Ruta para la página de inicio
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)