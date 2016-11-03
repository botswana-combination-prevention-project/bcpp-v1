from __future__ import absolute_import

import os
import sys

from celery import Celery
from unipath import Path

from django.conf import settings


SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(4)  # e.g. /home/django/source
EDC_DIR = SOURCE_ROOT.child('edc_project')  # e.g. /home/django/source/edc_project/
LIS_DIR = SOURCE_ROOT.child('lis_project')  # e.g. /home/django/source/lis_project/

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(1, EDC_DIR)
sys.path.insert(1, LIS_DIR)

app = Celery('bhp066')
app.config_from_object('config.celery.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


if __name__ == '__main__':
    app.start()
