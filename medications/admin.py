from django.contrib import admin
from .models import Medication, Prescription
admin.site.register(Medication)
admin.site.register(Prescription)