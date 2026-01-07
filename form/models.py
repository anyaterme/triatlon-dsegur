from django.db import models
import uuid

# Create your models here.
class IncidentForm(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nif = models.CharField(max_length=20, default="")
    birth_date = models.DateField(blank=True, null=True)
    email = models.EmailField()
    incident_date = models.DateField()
    location = models.CharField(max_length=300)
    incident_time = models.TimeField()
    incident_description = models.TextField()
    injuries_sustained = models.TextField(blank=True, null=True)
    medical_center_visited = models.CharField(max_length=300, blank=True, null=True)
    talon_required = models.BooleanField(default=False)
    talon_number = models.CharField(max_length=100, blank=True, null=True)
    parte_required = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)
    domicilio = models.CharField(max_length=300, blank=True, null=True)
    localidad = models.CharField(max_length=200, blank=True, null=True)
    provincia = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"IncidentForm({self.first_name} {self.last_name}, {self.email}, {self.date_submitted})"