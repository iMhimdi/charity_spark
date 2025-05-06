"""
ASGI config for charity_spark_project project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'charity_spark_project.settings')

application = get_asgi_application()