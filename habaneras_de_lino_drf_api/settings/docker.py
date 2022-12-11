

import environ
from .base import *

DEBUG = True

env = environ.Env()
# reading env file
environ.Env.read_env()

SECRET_KEY = env("DOCKER_SECRET_KEY")
DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DOCKER_DB_NAME'),
        'USER': env('DOCKER_DB_USER'),
        'PASSWORD': env('DOCKER_DB_PASSWORD'),
        'HOST': env('DOCKER_DB_HOST'),
        'PORT': env('DOCKER_DB_PORT'),
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STRIPE_PUBLISHABLE_KEY=env("DOCKER_STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY=env("DOCKER_STRIPE_SECRET_KEY")
