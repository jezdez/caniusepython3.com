from .settings import *

SECRET_KEY = '42'

DEBUG = True

SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False

ALLOWED_HOSTS = [
    'lan.caniusepython3.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'postgres',
        'NAME': 'postgres',
        'USER': 'postgres'
    }
}

TEMPLATES[0]['OPTIONS']['debug'] = True
TEMPLATES[0]['OPTIONS']['loaders'] = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

PIPELINE['PIPELINE_ENABLED'] = False

