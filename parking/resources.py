from import_export import resources
from .models import Parking, Vehicle_Type, WorkerRole, Worker, UserParkingAssignment

class ParkingResource(resources.ModelResource):
    class Meta:
        model = Parking

class Vehicle_TypeResource(resources.ModelResource):
    class Meta:
        model = Vehicle_Type

class WorkerRoleResource(resources.ModelResource):
    class Meta:
        model = WorkerRole

class WorkerResource(resources.ModelResource):
    class Meta:
        model = Worker

class UserParkingAssignmentResource(resources.ModelResource):
    class Meta:
        model = UserParkingAssignment
