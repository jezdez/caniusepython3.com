"""
Django settings for ciupy3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

from configurations import Configuration, values
from pathlib import Path

here = Path(__file__).parent.resolve()
assets_dir = here.parent / 'assets'


class Common(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
    )

    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'raven.contrib.django.raven_compat',
        'pipeline',
        'admin_honeypot',
        'djangosecure',
        'pq',
        'rest_framework',
        'south',
        'easy_pjax',
        'ciupy3.checks',
    )

    MIDDLEWARE_CLASSES = (
        'djangosecure.middleware.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'ciupy3.urls'

    WSGI_APPLICATION = 'ciupy3.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue
    DATABASES = values.DatabaseURLValue('postgres://ciupy3@localhost/ciupy3')

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = False

    USE_L10N = False

    USE_TZ = True

    REST_FRAMEWORK = {
        # 'DEFAULT_PERMISSION_CLASSES': (
        #     'rest_framework.permissions.IsAdminUser',
        # ),
        'PAGINATE_BY': 10,
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            # 'rest_framework.renderers.BrowsableAPIRenderer',
            'rest_framework.renderers.TemplateHTMLRenderer',
        )
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    CACHES = values.CacheURLValue('hiredis://127.0.0.1:6381/0')

    MEDIA_ROOT = str(assets_dir / 'media')
    MEDIA_URL = '/a/m/'
    STATIC_ROOT = str(assets_dir / 'static')
    STATIC_URL = '/a/s/'

    STATICFILES_STORAGE = 'ciupy3.storage.GZIPCachedStorage'

    STATICFILES_DIRS = [
        os.path.join(os.path.dirname(__file__), 'foundation'),
    ]

    EMAIL = values.EmailURLValue('console://')
    DEFAULT_FROM_EMAIL = 'hello@caniusepython3.com'
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    SENTRY_URL = os.environ.get('SENTRY_URL')
    RAVEN_CONFIG = {
        'dsn': SENTRY_URL,
    }

    PIPELINE_CSS = {
        'styles': {
            'source_filenames': (
                'css/normalize.css',
                'css/foundation.min.css',
                'css/gh-fork-ribbon.css',
                'css/app.css',
            ),
            'output_filename': 'styles.css',
        },
    }

    PIPELINE_JS = {
        'scripts': {
            'source_filenames': (
                'js/vendor/jquery.js',
                'js/vendor/fastclick.js',
                'js/foundation.min.js',
                'js/jquery.pjax.js',
                'js/spin.min.js',
                'js/app.js',
            ),
            'output_filename': 'scripts.js',
        }
    }

    PIPELINE_CSS_COMPRESSOR = None
    PIPELINE_JS_COMPRESSOR = None


class Dev(Common):
    """
    The in-development settings and the default configuration.
    """
    pass


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    MEDIA_ROOT = '/home/jezdez/webapps/ciupy3_assets/m'
    STATIC_ROOT = '/home/jezdez/webapps/ciupy3_assets/s'

    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + (
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    )

    ALLOWED_HOSTS = ['caniusepython3.com']

    STATIC_URL = '//d2yo0abyhdvl2j.cloudfront.net/'
    PIPELINE_ENABLED = True
