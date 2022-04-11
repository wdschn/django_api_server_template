from .base import *

DEBUG = True

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.BasicAuthentication'
]
