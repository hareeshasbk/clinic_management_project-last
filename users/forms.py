from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.validators import RegexValidator
from django.utils.html import escape

class UserEditForm(forms.ModelForm):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('receptionist', 'Receptionist'),
    )
    role = forms.ChoiceField(choices=USER_ROLES, label="Role")

    class Meta:
        model = User
        fields = ['role']