from .base import *

DEBUG = True

INSTALLED_APPS += [
    'drf_yasg',
]

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.BasicAuthentication'
]
