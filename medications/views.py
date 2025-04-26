from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MedicationForm, PrescriptionForm
from .models import Medication, Prescription
from django.contrib import messages
from users.decorators import allowed_roles
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model()

# Medication Management Views

@login_required
@allowed_roles(roles=['admin', 'doctor'])
def medication_list(request):

    medications = Medication.objects.all()
    return render(request, 'medications/medication_list.html', {'medications': medications})

@login_required
@allowed_roles(roles=['admin', 'doctor'])  # Add 'doctor' to allowed roles
def medication_create(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save()
            messages.success(request, 'Medication created successfully!')
            if request.user.role == 'doctor':
                return redirect('doctor_dashboard')  # Redirect doctors to their dashboard
            return redirect('medications:medication_list')
    else:
        form = MedicationForm()
    return render(request, 'medications/medication_form.html', {
        'form': form,
        'title': 'Create New Medication'
    })

# Update the medication_edit decorator to allow doctors
@login_required
@allowed_roles(roles=['admin', 'doctor'])  # Add 'doctor' to allowed roles
def medication_edit(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medication updated successfully!')
            if request.user.role == 'doctor':
                return redirect('doctor_dashboard')  # Redirect doctors to their dashboard
            return redirect('medications:medication_list')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'medications/medication_form.html', {'form': form, 'medication': medication})

# Update the medication_delete decorator to allow doctors
@login_required
@allowed_roles(roles=['admin', 'doctor'])  # Add 'doctor' to allowed roles 
def medication_delete(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        medication.delete()
        messages.success(request, 'Medication deleted successfully!')
        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')  # Redirect doctors to their dashboard
        return redirect('medications:medication_list')
    return render(request, 'medications/medication_confirm_delete.html', {'medication': medication})

# Prescription Management Views

@login_required
@allowed_roles(roles=['doctor'])
def prescription_create(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user  # Set the doctor to the current user
            prescription.save()
            messages.success(request, 'Prescription created successfully!')
            return redirect('medications:prescription_list')
    else:
        form = PrescriptionForm()
    return render(request, 'medications/prescription_form.html', {'form': form})

@login_required
@allowed_roles(roles=['doctor', 'admin'])
def prescription_list(request):
    if request.user.role == 'doctor':
        prescriptions = Prescription.objects.filter(doctor=request.user)
    else:
         prescriptions = Prescription.objects.all() #show all prescriptions
    return render(request, 'medications/prescription_list.html', {'prescriptions': prescriptions})

@login_required
@allowed_roles(roles=['doctor'])
def patient_list(request):
    # Update to use correct related name 'prescriptions'
    patients = User.objects.filter(role='patient').annotate(
        prescription_count=Count('prescriptions')  # Changed from patient_prescriptions to prescriptions
    ).order_by('first_name')
    
    return render(request, 'medications/patient_list.html', {
        'patients': patients
    })

@login_required
@allowed_roles(roles=['doctor'])
def patient_detail(request, pk):
    patient = get_object_or_404(User, pk=pk)
    prescriptions = Prescription.objects.filter(
        patient=patient,
        doctor=request.user
    ).order_by('-date_prescribed')
    
    context = {
        'patient': patient,
        'prescriptions': prescriptions,
    }
    return render(request, 'medications/patient_detail.html', context)
