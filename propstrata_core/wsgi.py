"""WSGI config for PropStrata project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "propstrata_core.settings")

application = get_wsgi_application()
