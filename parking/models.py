from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vehicle_Type(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

class Parking(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

class WorkerRole(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.name)

class Worker(models.Model):
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    code = models.CharField(max_length=8, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT)
    role = models.ForeignKey(WorkerRole, null=True, blank=True, on_delete=models.RESTRICT)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return str(self.code) + " - " + self.first_name + " " + self.last_name

class UserParkingAssignment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assigned_parking')
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} asignado a {self.parking.name}"