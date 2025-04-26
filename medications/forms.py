from django import forms
from .models import Medication, Prescription
from django.utils.html import escape
from django.contrib.auth import get_user_model

User = get_user_model()

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'description', 'quantity_in_stock', 'reorder_level']  # Added new fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control'}),  # Added widget
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),  # Added widget
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = escape(name)
        return name

    def clean_dosage(self):
        dosage = self.cleaned_data.get('dosage')
        if dosage:
            dosage = escape(dosage)
        return dosage

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description:
            description = escape(description)
        return description


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medication', 'dosage', 'frequency', 'instructions']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'medication': forms.Select(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Override the init to set the queryset for the patient field to only be patients.
        """
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.objects.filter(role='patient')

    def clean_dosage(self):
        dosage = self.cleaned_data.get('dosage')
        if dosage:
            dosage = escape(dosage)
        return dosage

    def clean_frequency(self):
        frequency = self.cleaned_data.get('frequency')
        if frequency:
            frequency = escape(frequency)
        return frequency

    def clean_instructions(self):
        instructions = self.cleaned_data.get('instructions')
        if instructions:
            instructions = escape(instructions)
        return instructions