from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView

class TwoFactorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Skip 2FA for certain paths
            excluded_paths = [
                reverse('verify_email_2fa'),
                reverse('logout'),
                '/admin/',  # Skip for admin
            ]
            
            if not request.path in excluded_paths and not request.session.get('email_2fa_verified'):
                return redirect('verify_email_2fa')

        response = self.get_response(request)
        return response