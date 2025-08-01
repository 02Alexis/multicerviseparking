from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from multi_service_parking.middleware import login_exempt

@login_exempt
def login_view(request):

    # Si el usuario ya está autenticado, redirige a la página principal (home)
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('settlement_chart')  # Redirige al home si ya está autenticado

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)  # Iniciar sesión
            messages.success(request, f"Bienvenido {user.username}")
            return redirect('settlement_chart')  # Redirige a la página de inicio después de iniciar sesión
        else:
            messages.error(request, "Usuario o contraseña no válidos")

    return render(request, 'users/login.html', {
        'title': 'Inicio'
    })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('settlement_chart')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Verificar si es el primer usuario registrado
            if User.objects.count() == 0:
                user.is_superuser = True
                user.is_staff = True
            else:
                user.is_superuser = False
                user.is_staff = False
            
            user.save()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}, tu cuenta ha sido creada.")
            return redirect('settlement_chart')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form, 'title': 'Registro'})
@login_exempt
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada')
    return redirect('login')


def account(request):
    return render(request, 'account.html', {
        'title': 'Perfil'
    })
