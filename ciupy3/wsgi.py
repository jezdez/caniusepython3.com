import os
# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "ciupy3.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ciupy3.settings")

if os.environ['DJANGO_SETTINGS_MODULE'].endswith('prod'):
    import newrelic.agent
    newrelic.agent.initialize()

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(get_wsgi_application())
