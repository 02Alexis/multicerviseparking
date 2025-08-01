<a name="readme-top"></a>

<details>
<summary>Tabla de contenidos</summary>

1. [Creación del entorno virtual y configuración](#creación-del-entorno-virtual-y-configuración)
2. [Para empezar](#para-empezar)
   - [Instalar Django](#instalar-django)
   - [Planes segun capacidad operativa](#planes-segun-capacidad-operativa)

</details>

> [!NOTE]
> # Creación del entorno virtual y configuración 
 
## 1. Sigue los pasos a continuación para configurar y activar un entorno virtual:

```bash
$ py -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

# Para empezar
# Instalar Django.
> [!IMPORTANT]
> Con el entorno virtual activado, instala Django: <a href="https://docs.djangoproject.com/en/5.2/intro/tutorial01/" target="_blank"> Django Doc</a></p>

```bash
python -m pip install Django

# Verifica la instalación con:
python -m django --version
```


## 3. Crear un Nuevo Proyecto Django.

    django-admin startproject mi_proyecto

# La estructura generada será similar a:
```bash
mi_proyecto/
│── manage.py
│── mi_proyecto/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

## 4. Ejecuta el siguiente comando para iniciar el servidor local:

    $ python manage.py runserver

## 5. Crear una Aplicación dentro del Proyecto

    python manage.py startapp mi_app

# La estructura generada será similar a:
```bash
mi_app/
│── migrations/
│── __init__.py
│── admin.py
│── apps.py
│── models.py
│── tests.py
│── views.py

```

## 6. Configurar la Aplicación.
```bash
INSTALLED_APPS = [
    # Otras aplicaciones predeterminadas
    'mi_app',
]
```

## 7. Realizar Migraciones de la Base de Datos
```bash
# Configura la base de datos creando y aplicando las migraciones:
python manage.py makemigrations
python manage.py migrate

```

## 
<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

> [!TIP]
> # Generar el archivo automáticamente

Si ya tienes un entorno virtual con las dependencias instaladas, puedes generar el archivo requirements.txt ejecutando el siguiente comando dentro del entorno virtual:

    pip freeze > requirements.txt

# Instalación de dependencias
Asegúrate de tener el entorno virtual activo y ejecuta el siguiente comando para instalar las dependencias del proyecto:

    pip install -r requirements.txt

<p align="right">(<a href="#readme-top">volver arriba</a>)</p>

# Planes segun capacidad operativa

### 1. Plan Básico (Hasta 2 parqueaderos)
- Límite de 50 clientes mensuales registrados (`Customer`)
- 3 usuarios administrativos (`UserParkingAssignment`)
- Soporte por correo electrónico (respuesta en 24h)
- Capacitación inicial vía documentación técnica
- Facturación básica (`Invoice`) con hasta 5 productos por transacción
- Reportes de liquidaciones diarias (`Settlement`) sin historial

### 2. Plan Profesional (Hasta 5 parqueaderos)
- 200 clientes con estados personalizables (`status` field)
- 10 usuarios con roles diferenciados (`WorkerRole`)
- Soporte prioritario por chat (+ memoria de despliegue)
- Capacitación mensual en vivo (2 horas)
- Facturación avanzada con NIT y documentos legales (`DOCUMENT_TYPE_CHOICES`)
- Historial de liquidaciones por 6 meses

### 3. Plan Empresarial (Parqueaderos ilimitados)
- Clientes ilimitados con placa personalizada (`formatted_license_plate`)
- Usuarios ilimitados con control de modificaciones (`modified_by`)
- Soporte 24/7 con acceso a servidor (reinicios programados)
- Capacitación semanal y manuales personalizados
- Liquidaciones automáticas (`calculate_amounts`) con múltiples porcentajes
- Integración con pasarelas de pago (extensión del modelo `Invoice`)

---

## Características técnicas por modelo

| Modelo     | Plan Básico           | Plan Profesional           | Plan Empresarial            |
|------------|----------------------|---------------------------|----------------------------|
| Parking    | 2 instancias         | 5 con geolocalización     | Ilimitados + dashboard     |
| Settlement | Cálculo manual       | Automático diario         | En tiempo real + ARM       |
| Customer   | 3 estados fijos      | 5 estados personalizables | Flujos de trabajo          |
| Invoice    | PDF básico           | Plantillas editable       | Firmas digitales           |


   ## 🛠️ Stack

[![My Skills](https://skillicons.dev/icons?i=py,sqlite,django,html,jquery,)](https://skillicons.dev)
