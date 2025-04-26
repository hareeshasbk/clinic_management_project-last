from django import forms
from allauth.account.forms import SignupForm
from django.core.validators import RegexValidator
from django.utils.html import escape


class CustomSignupForm(SignupForm):
    USER_ROLES = (
        ('patient', 'Patient'),
    )
    role = forms.ChoiceField(choices=USER_ROLES, label="Role")
    first_name = forms.CharField(
        max_length=100,
        label="First Name",
        validators=[
            RegexValidator(
                r'^[a-zA-Z\s]*$',
                'Only letters and spaces are allowed.'
            )
        ]
    )
    last_name = forms.CharField(
        max_length=100,
        label="Last Name",
        validators=[
            RegexValidator(
                r'^[a-zA-Z\s]*$',
                'Only letters and spaces are allowed.'
            )
        ]
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        user.save()
        return user