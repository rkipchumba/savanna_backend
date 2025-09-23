"""
Django settings for savannah_backend project.
"""

from pathlib import Path
import warnings


BASE_DIR = Path(__file__).resolve().parent.parent

warnings.filterwarnings(
    "ignore",
    message=".*app_settings.(USERNAME_REQUIRED|EMAIL_REQUIRED) is deprecated.*"
)

SECRET_KEY = 'django-insecure-(63rurtw#p9#tz#8%9^n=vi^8h=+6e8yz003cagxswo$3=fqsr'
DEBUG = True
ALLOWED_HOSTS = []

AT_USERNAME = "sandbox"
AT_API_KEY = "atsk_ee8686925336242625cb7455e1a780838508c71cbceca1364e521cb5ca2c6151d71553f0"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'allauth.socialaccount.providers.google',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',

    # My apps
    'customers',
    'products',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'savannah_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "orders.context_processors.cart_item_count",
            ],
        },
    },
]

WSGI_APPLICATION = 'savannah_backend.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'savannah_db',
        'USER': 'savannah_user',
        'PASSWORD': 'savannah_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# REST Framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# Django Allauth settings
SITE_ID = 1
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
SOCIALACCOUNT_AUTO_SIGNUP = True 
ACCOUNT_EMAIL_VERIFICATION = "none"





# Tell dj-rest-auth to use allauth
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "customers.serializers.CustomerSerializer",
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default PK type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google OAuth2
GOOGLE_CALLBACK_URL = "http://127.0.0.1:8000/auth/google/callback/"
LOGIN_REDIRECT_URL = '/products/'  
LOGOUT_REDIRECT_URL = '/products/'

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "kipchumbarodgers@gmail.com"
EMAIL_HOST_PASSWORD = "trzk fnpx lykr zudo"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
