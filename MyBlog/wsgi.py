"""
WSGI config for MyBlog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

from os.path import join,dirname,abspath
PROJECT_DIR = dirname(dirname(abspath(__file__)))

import sys
import os
from settings import DJANGO_RELEASE, DJANGO_SETTINGS_MODULE
sys.path.insert(0, PROJECT_DIR)
os.environ.setdefault(DJANGO_SETTINGS_MODULE, "MyBlog.settings")
os.environ.setdefault(DJANGO_RELEASE, "")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
