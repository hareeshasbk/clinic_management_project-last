from django import forms
from .models import Appointment
from django_flatpickr.widgets import DatePickerInput, TimePickerInput
from django.contrib.auth import get_user_model
from django_flatpickr.schemas import FlatpickrOptions

User = get_user_model()

date_options = FlatpickrOptions(
    altFormat="F j, Y",
    minDate="today",
    allowInput=True
)

time_options = FlatpickrOptions(
    time_24hr=True,
    minuteIncrement=30,
    minTime="09:00",
    maxTime="18:00"
)

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='doctor'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'reason']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'date': DatePickerInput(
                attrs={'class': 'form-control'},
                options=date_options
            ),
            'time': TimePickerInput(
                attrs={'class': 'form-control'},
                options=time_options
            ),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'reason']
        widgets = {
            'date': DatePickerInput(
                attrs={'class': 'form-control'},
                options=date_options
            ),
            'time': TimePickerInput(
                attrs={'class': 'form-control'},
                options=time_options
            ),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
