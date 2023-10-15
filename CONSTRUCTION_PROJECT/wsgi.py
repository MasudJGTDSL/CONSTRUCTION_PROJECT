"""
WSGI config for CONSTRUCTION_PROJECT project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .settings import base

if base.DEBUG == True:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONSTRUCTION_PROJECT.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONSTRUCTION_PROJECT.settings.production")

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONSTRUCTION_PROJECT.settings')

application = get_wsgi_application()
