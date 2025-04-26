import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from appointments.models import Appointment
from medications.models import Prescription
from .forms import UserEditForm
from .decorators import allowed_roles
from django import forms
from .models import User
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerificationCode

# Get a logger instance
logger = logging.getLogger(__name__)
User = get_user_model()

class AdminUserCreationForm(UserCreationForm):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('receptionist', 'Receptionist'),
    )
    role = forms.ChoiceField(choices=USER_ROLES, label="Role")

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

@login_required
@allowed_roles(roles=['admin'])
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)  # Get the user object or return a 404 error
    form = UserEditForm(instance=user)  # Initialize form for GET requests
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)  # Pass the user instance to the form
        if form.is_valid():
            form.save()
            messages.success(request, f'Role updated for {user.username}!')
            return redirect('user_list')

    return render(request, 'users/user_edit.html', {'form': form, 'user': user})


@login_required
@allowed_roles(roles=['admin'])
def user_list(request):
    users = User.objects.all()  # Get all users from the database
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@allowed_roles(roles=['admin'])
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')


@login_required
@allowed_roles(roles=['patient'])
def patient_dashboard(request):
    patient = get_object_or_404(User, pk=request.user.id)
    prescriptions = Prescription.objects.filter(patient=patient)
    return render(request, 'users/patient_dashboard.html', {'patient': patient, 'prescriptions': prescriptions})

@login_required
@allowed_roles(roles=['receptionist'])
def receptionist_dashboard(request):
    return render(request, 'users/receptionist_dashboard.html')

# Remove these functions as they're no longer needed:
# - generate_backup_codes
# - verify_backup_code
# - two_factor_setup
# - two_factor_verify
# - two_factor_disable
# - check_2fa_status

# Update custom_login to remove 2FA checks
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            logger.info(f'User {user.email} logged in successfully.')
            return redirect('home')
        else:
            logger.warning(f'Failed login attempt with username: {form.data.get("username")}. Errors: {form.errors}')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def home(request):
    """Redirect users to their appropriate dashboard based on their role."""
        
    role_redirects = {
        'admin': 'admin_dashboard',
        'doctor': 'doctor_dashboard',
        'patient': 'patient_dashboard',
        'receptionist': 'receptionist_dashboard'
    }
    
    redirect_url = role_redirects.get(request.user.role)
    if redirect_url:
        return redirect(redirect_url)
    
    return render(request, 'users/home.html')

@login_required
@allowed_roles(roles=['admin'])
def create_admin_user(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('user_list')
    else:
        form = AdminUserCreationForm()
    return render(request, 'users/create_admin_user.html', {'form': form})


@login_required
@allowed_roles(roles=['admin'])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'User {user.username} deleted.')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

@login_required
@allowed_roles(roles=['admin'])
def user_deactivate(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f'User {user.username} deactivated.')
        return redirect('user_list')
    return render(request, 'users/user_confirm_deactivate.html', {'user': user})


@login_required
@allowed_roles(roles=['admin'])
def user_activate(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = True
        user.save()
        messages.success(request, f'User {user.username} activated.')
        return redirect('user_list')
    return render(request, 'users/user_confirm_activate.html', {'user': user})

@login_required
@allowed_roles(roles=['doctor'])
def doctor_dashboard(request):
    doctor = request.user
    
    # Get appointments
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    
    # Get medication-related data
    recent_prescriptions = Prescription.objects.filter(doctor=doctor).order_by('-date_prescribed')[:5]
    total_patients = User.objects.filter(role='patient').count()
    total_prescriptions = Prescription.objects.filter(doctor=doctor).count()
    
    # Get most prescribed medication
    from django.db.models import Count
    most_prescribed = Prescription.objects.filter(doctor=doctor) \
        .values('medication__name') \
        .annotate(total=Count('medication')) \
        .order_by('-total') \
        .first()
    
    most_prescribed_medication = most_prescribed['medication__name'] if most_prescribed else None
    
    context = {
        'appointments': appointments,
        'recent_prescriptions': recent_prescriptions,
        'total_patients': total_patients,
        'total_prescriptions': total_prescriptions,
        'most_prescribed_medication': most_prescribed_medication
    }
    
    return render(request, 'users/doctor_dashboard.html', context)

@login_required
def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('home')
    return render(request, 'users/logout.html')

@login_required
def verify_email_2fa(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        stored_code = EmailVerificationCode.objects.filter(
            user=request.user,
            is_used=False
        ).order_by('-created_at').first()

        if stored_code and stored_code.code == entered_code:
            stored_code.is_used = True
            stored_code.save()
            request.session['email_2fa_verified'] = True
            return redirect('home')  # Replace with your home view
        else:
            messages.error(request, 'Invalid verification code')
            return render(request, 'users/verify_2fa.html')

    # Generate and send new code
    verification_code = EmailVerificationCode.generate_code()
    EmailVerificationCode.objects.create(
        user=request.user,
        code=verification_code
    )

    # Send email with code
    send_mail(
        'Your 2FA Verification Code',
        f'Your verification code is: {verification_code}',
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False,
    )

    return render(request, 'users/verify_2fa.html')