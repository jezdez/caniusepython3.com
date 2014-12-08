"""
The in-production settings.
"""
import os
from .common import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

MIDDLEWARE_CLASSES += (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
)

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

ALLOWED_HOSTS = ['*']

PIPELINE_ENABLED = True

STATIC_URL = '/assets/static/'
MEDIA_URL = '/assets/media/'

SENTRY_URL = os.environ.get('SENTRY_URL')
RAVEN_CONFIG = {
    'dsn': SENTRY_URL,
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
