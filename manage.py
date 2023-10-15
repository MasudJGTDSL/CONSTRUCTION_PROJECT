#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from CONSTRUCTION_PROJECT.settings import base

def main():
    """Run administrative tasks."""
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONSTRUCTION_PROJECT.settings')
    if base.DEBUG == True:
            # print("Debug is: True")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONSTRUCTION_PROJECT.settings.local")
    else:
        # print("Debug is: False")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CONSTRUCTION_PROJECT.settings.production")
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
