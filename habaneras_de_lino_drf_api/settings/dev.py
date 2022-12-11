import environ
from .base import *
import cloudinary
import cloudinary.uploader
import cloudinary.api

DEBUG = True

env = environ.Env()
# reading env file
environ.Env.read_env()

SECRET_KEY = env("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

STRIPE_PUBLIC_KEY=env("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY=env("STRIPE_SECRET_KEY")

cloudinary.config(
  cloud_name = env('CLOUDINARY_CLOUD_NAME'),
  api_key = env('CLOUDINARY_API_KEY'),
  api_secret = env('CLOUDINARY_API_SECRET')
)

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
