"""
Django settings for ciupy3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

from configurations import Configuration, values


class Common(Configuration):

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')07khcog6b!)x636@=%rq53mk0g-^!n_p(jf!2bfhyc-*5^f_9'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'pq',
        'rest_framework',
    )

    MIDDLEWARE_CLASSES = (
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
    DATABASES = values.DatabaseURLValue('sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'))

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = False

    USE_L10N = False

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_URL = '/static/'

    REST_FRAMEWORK = {
        # 'DEFAULT_PERMISSION_CLASSES': (
        #     'rest_framework.permissions.IsAdminUser',
        # ),
        'PAGINATE_BY': 10,
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
            'rest_framework.renderers.TemplateHTMLRenderer',
        )
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '[%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': "logging.StreamHandler",
                'formatter': 'standard'
            },
        },
        'loggers': {
            'pq': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True
            },
        }
    }

    CACHES = values.CacheURLValue('hiredis://127.0.0.1:6381/0')


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

    SECRET_KEY = values.SecretValue()
