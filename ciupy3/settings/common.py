"""
Django settings for ciupy3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from pathlib import Path

here = Path(__file__).parent.parent.resolve()
assets_dir = here.parent / 'assets'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(here.parent)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')07khcog6b!)x636@=%rq53mk0g-^!n_p(jf!2bfhyc-*5^f_9'

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

TEMPLATE_DIRS = [
    str(here / 'templates'),
]

ALLOWED_HOSTS = []

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
    'admin_honeypot',
    'djangosecure',
    'django_rq',
    'rest_framework',
    'south',
    'easy_pjax',
    'whitenoise',
    'macros',
    'staticflatpages',
    'ciupy3.checks',
)

MIDDLEWARE_CLASSES = (
    'hirefire.contrib.django.middleware.HireFireMiddleware',
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
        'USER': 'ciupy3',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
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
    )
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:0',
        'OPTIONS': {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        }
    }
}

MEDIA_ROOT = str(assets_dir / 'media')
MEDIA_URL = '/assets/media/'
STATIC_ROOT = str(assets_dir / 'static')
STATIC_URL = '/assets/static/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_DIRS = [
    str(here / 'foundation'),
]

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
            'js/jquery.textcomplete.min.js',
            'js/jquery.pjax.js',
            'js/jquery.autosize.min.js',
            'js/app.js',
        ),
        'output_filename': 'scripts.js',
    }
}

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

HIREFIRE_PROCS = [
    'ciupy3.procs.WorkerProc',
    'ciupy3.procs.HighWorkerProc',
]

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
        }
    }
}

RQ_QUEUES = {
    'high': {
        'USE_REDIS_CACHE': 'default',
    },
    'default': {
        'USE_REDIS_CACHE': 'default',
    },
    'low': {
        'USE_REDIS_CACHE': 'default',
    },
}
RQ_SHOW_ADMIN_LINK = True
