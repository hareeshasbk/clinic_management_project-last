from django.db import models
from django.conf import settings

class Medication(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, blank=True, null=True)  # e.g., "500mg", "1 tablet"
    description = models.TextField(blank=True, null=True)
    quantity_in_stock = models.IntegerField(default=0)  # New field: Quantity in stock
    reorder_level = models.IntegerField(default=10)  # New field: Reorder level
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescribed_medications')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100, blank=True, null=True)  # Specific dosage for this prescription
    frequency = models.CharField(max_length=255, blank=True, null=True)  # e.g., "Twice a day", "Every 8 hours"
    instructions = models.TextField(blank=True, null=True)  # Additional instructions for the patient
    date_prescribed = models.DateField(auto_now_add=True)  # Automatically set the date when the prescription is created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient.email} - {self.medication.name}"
    