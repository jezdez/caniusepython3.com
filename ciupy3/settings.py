"""
Django settings for ciupy3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
from celery.schedules import crontab
from kombu import Queue, Exchange
from pathlib import Path

here = Path(__file__).parent.resolve()
assets_dir = here.parent / 'assets'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(here.parent)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

ALLOWED_HOSTS = [
    'caniusepython3.com'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(here / 'templates')
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': False,
            "builtins": [
                "easy_pjax.templatetags.pjax_tags"
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            )
        },
    },
]

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'pipeline',
    # 'admin_honeypot',  # FIXME: Doesn't work with Django 1.9 yet
    'djangosecure',
    'rest_framework',
    'easy_pjax',
    'whitenoise',
    'staticflatpages',
    'ciupy3.checks',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'staticflatpages.middleware.StaticFlatpageFallbackMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easy_pjax.middleware.UnpjaxMiddleware'
)

ROOT_URLCONF = 'ciupy3.urls'

WSGI_APPLICATION = 'ciupy3.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ciupy3',
        'USER': 'ciupy3',
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Prague'

USE_I18N = False

USE_L10N = False

USE_TZ = True

REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
        'ciupy3.checks.renderers.SVGRenderer',
        'ciupy3.checks.renderers.PNGRenderer',
    ),
    'DATETIME_FORMAT': None,
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
    }
}

MEDIA_ROOT = str(assets_dir / 'media')
MEDIA_URL = '/assets/media/'
STATIC_ROOT = str(assets_dir / 'static')
STATIC_URL = '/assets/static/'

STATICFILES_STORAGE = 'ciupy3.storage.GzipManifestPipelineStorage'

STATICFILES_DIRS = [
    str(here / 'foundation'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'PIPELINE_ENABLED': True,

    'STYLESHEETS': {
        'styles': {
            'source_filenames': (
                'css/normalize.css',
                'css/foundation.min.css',
                'css/gh-fork-ribbon.css',
                'css/app.css',
            ),
            'output_filename': 'styles.css',
        },
    },

    'JAVASCRIPT': {
        'scripts': {
            'source_filenames': (
                'js/vendor/jquery.js',
                'js/vendor/fastclick.js',
                'js/foundation.min.js',
                'js/jquery.textcomplete.min.js',
                'js/jquery.pjax.js',
                'js/jquery.autosize.min.js',
                'js/app.js',
            ),
            'output_filename': 'scripts.js',
        }
    },

    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None

}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'ciu': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'redis_lock': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    }
}

BROKER_URL = 'redis://redis:6379/0'
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

CELERY_RESULT_BACKEND = 'redis://redis:6379/2'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)
CELERY_ROUTES = {
    'ciupy3.checks.tasks.run_check': {'queue': 'high'},
    'ciupy3.checks.tasks.check_all_projects': {'queue': 'high'},
}

every_10_minutes = crontab(minute='*/10')
CELERYBEAT_SCHEDULE = {
    'fetch_all_projects': {
        'task': 'ciupy3.checks.tasks.fetch_all_projects',
        'schedule': crontab(minute='35'),
    },
    'fill_autocomplete_index': {
        'task': 'ciupy3.checks.tasks.fill_autocomplete_index',
        'schedule': crontab(minute='55'),
    },
    'update_checked_count': {
        'task': 'ciupy3.checks.tasks.update_checked_count',
        'schedule': every_10_minutes,
    },
}
