from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm, AppointmentEditForm
from .models import Appointment
from django.contrib import messages
from users.decorators import allowed_roles

@login_required
@allowed_roles(roles=['receptionist'])
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})


@login_required
@allowed_roles(roles=['receptionist'])
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created successfully!')
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {'form': form})


@login_required
@allowed_roles(roles=['receptionist', 'admin', 'doctor'])
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        if request.user.role == 'doctor':
            form = AppointmentEditForm(request.POST, instance=appointment)
        else:
            form = AppointmentForm(request.POST, instance=appointment)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            if request.user.role == 'doctor':
                return redirect('doctor_dashboard')
            return redirect('appointments:appointment_list')
    else:
        if request.user.role == 'doctor':
            form = AppointmentEditForm(instance=appointment)
        else:
            form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_edit.html', {'form': form, 'appointment': appointment})



@login_required
@allowed_roles(roles=['receptionist', 'admin', 'doctor'])  # Add 'doctor' to allowed roles
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully!')
        if request.user.role == 'doctor':
            return redirect('doctor_dashboard')  # Redirect doctors back to their dashboard
        return redirect('appointments:appointment_list')  # For other roles
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})



# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from users.decorators import allowed_roles
# from .models import Appointment
# from .forms import AppointmentEditForm  # Import the AppointmentEditForm


# @login_required
# @allowed_roles(roles=['doctor'])
# def appointment_edit(request, pk):
#     appointment = get_object_or_404(Appointment, pk=pk)  # Get the appointment object or return a 404 error
#     if request.method == 'POST':
#         form = AppointmentEditForm(request.POST, instance=appointment)  # Pass the appointment instance to the form
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Appointment rescheduled successfully!')
#             return redirect('doctor_dashboard')
#     else:
#         form = AppointmentEditForm(instance=appointment)  # Pass the appointment instance to the form
#     return render(request, 'appointments/appointment_edit.html', {'form': form, 'appointment': appointment})


# @login_required
# @allowed_roles(roles=['doctor'])
# def appointment_cancel(request, pk):
#     appointment = get_object_or_404(Appointment, pk=pk)
#     if request.method == 'POST':
#         appointment.delete()
#         messages.success(request, "Appointment Cancelled")
#         return redirect('doctor_dashboard')

#     return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})
