import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'web']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required by allauth

    # Third party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap5',  # Add this line
    'django_bootstrap5',
    'django_flatpickr',

    # Local apps
    'users',
    'appointments',
    'medications',
]

# Add this line after INSTALLED_APPS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # allauth middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.TwoFactorMiddleware',
]

ROOT_URLCONF = 'clinic_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'django_bootstrap5.templatetags.django_bootstrap5'
            ]

        },
    },
]

WSGI_APPLICATION = 'clinic_management.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"  # Redirect to home page after login

# Add this line 
LOGIN_URL = 'account_login'  # Specify the login URL

# Account settings
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Requires email verification
ACCOUNT_LOGIN_METHODS = {'email'}

ACCOUNT_USERNAME_REQUIRED = False  # no need for username
ACCOUNT_EMAIL_REQUIRED = True  # email is compulsory

ACCOUNT_LOGOUT_REDIRECT_URL = '/'  # Redirect to home page after logout
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # Prompt for password confirmation during signup

ACCOUNT_RATE_LIMITS = {
    'login_failed': (5, 300),  # 5 attempts in 300 seconds
}

# Add these settings
ACCOUNT_SIGNUP_REDIRECT_URL = "/"  # Redirect to home page after signup
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # Redirect to home page after logout
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hareesh@gmail.com'
EMAIL_HOST_PASSWORD = 'qfae aphy osee bmve'

# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    }
}

AUTH_USER_MODEL = 'users.User'

# ACCOUNT_FORMS = {'signup': 'users.forms.UserRegisterForm'} #Remove this line
ACCOUNT_FORMS = {
    'signup': 'users.custom_forms.CustomSignupForm'
}


CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']


# 

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True

# 'medications.views': {  # Replace 'your_app' with the name of your app


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard'
#         },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'clinic_management.log',
#             'formatter': 'standard'
#         },
#     },
#     'loggers': {
#         'users.views': {
#             'handlers': ['console', 'file'],
#             'level': 'INFO',
#             'propagate': True
#         },
#         '': {  # root logger
#             'handlers': ['console', 'file'],
#             'level': 'WARNING',
#         },
#     },
# }


# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5  # limit login attempts
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutes

# For development/testing, you can use the console backend:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'