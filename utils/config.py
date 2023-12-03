import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file
env_file = Path(__file__).resolve().parent.parent / "envs" / ".env"
load_dotenv(env_file)

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Static
STATIC_URL = os.getenv('STATIC_URL')
MEDIA_URL = os.getenv('MEDIA_URL')
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv('MEDIA_ROOT'))
# Secret Key
SECRET_KEY = os.getenv('SECRET_KEY')

# Debug
DEBUG = os.getenv('DEBUG')

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Email settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))

# redis
BROKER_URL = os.getenv('BROKER_URL')
# Internationalization
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')
TIME_ZONE = os.getenv('TIME_ZONE')
USE_I18N = os.getenv('USE_I18N')
USE_TZ = os.getenv('USE_TZ')
# cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('LOCATION'),
        'TIMEOUT': 'TIMEOUT',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }

    }
}
# swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
