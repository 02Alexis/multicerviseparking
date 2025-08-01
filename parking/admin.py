from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import ParkingResource, Vehicle_TypeResource, WorkerResource, WorkerRoleResource, UserParkingAssignmentResource
from .models import Parking, WorkerRole, Worker, Vehicle_Type, UserParkingAssignment

# Register your models here.
@admin.register(Parking)
class ParkingAdmin(ImportExportModelAdmin):
    resource_class = ParkingResource
    list_display = ('name', 'address', 'created_at', 'created_by')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'created_by')

@admin.register(Vehicle_Type)
class Vehicle_TypeAdmin(ImportExportModelAdmin):
    resource_class = Vehicle_TypeResource
    list_display = ('name', 'created_at', 'created_by')
    search_fields = ('name',)
    list_filter = ('created_at', 'created_by')

@admin.register(WorkerRole)
class WorkerRoleAdmin(ImportExportModelAdmin):
    resource_class = WorkerRoleResource
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Worker)
class WorkerAdmin(ImportExportModelAdmin):
    resource_class = WorkerResource
    search_fields = ("first_name", "last_name", "code")
    list_filter = ('created_at', 'created_by')

@admin.register(UserParkingAssignment)
class UserParkingAssignmentAdmin(ImportExportModelAdmin):
    resource_class = UserParkingAssignmentResource
    list_display = ('user', 'parking')
    search_fields = ('user__username', 'parking__name')
    list_filter = ('user', 'parking')
