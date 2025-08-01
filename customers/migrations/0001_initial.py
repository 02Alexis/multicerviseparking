# Generated by Django 5.1.7 on 2025-04-03 01:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('vehicle', models.CharField(choices=[('MOTO', 'Moto'), ('AUTOMOVIL', 'Automóvil'), ('TURBO', 'Turbo'), ('CAMIONETA', 'Camioneta'), ('CARRITO', 'Carrito')], max_length=10)),
                ('license_plate', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('payment_day', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parking_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='parking.parking')),
            ],
        ),
    ]
