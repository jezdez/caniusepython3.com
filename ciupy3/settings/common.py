"""
Django settings for ciupy3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from celery.schedules import crontab
from kombu import Queue, Exchange
from pathlib import Path

here = Path(__file__).parent.parent.resolve()
assets_dir = here.parent / 'assets'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(here.parent)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '42'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(here / 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',
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
)

ROOT_URLCONF = 'ciupy3.urls'

WSGI_APPLICATION = 'ciupy3.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ciupy3',
        'USER': 'ciupy3'
    }
}

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
        'ciupy3.checks.renderers.SVGRenderer',
        'ciupy3.checks.renderers.PNGRenderer',
    ),
    'DATETIME_FORMAT': None,
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        # 'OPTIONS': {
        #     'PARSER_CLASS': 'redis.connection.HiredisParser',
        # }
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
    'PIPELINE_ENABLED': False,

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

BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_TRANSPORT_OPTIONS = {'fanout_patterns': True}

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
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
    'fetch_all_py3_projects': {
        'task': 'ciupy3.checks.tasks.fetch_all_py3_projects',
        'schedule': every_10_minutes,
    },
    'fetch_all_projects': {
        'task': 'ciupy3.checks.tasks.fetch_all_projects',
        'schedule': crontab(minute='35'),
    },
    'fetch_overrides': {
        'task': 'ciupy3.checks.tasks.fetch_overrides',
        'schedule': every_10_minutes,
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
CELERY_ACCEPT_CONTENT = ['pickle']
CELERYD_FORCE_EXECV = True
