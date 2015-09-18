#!/usr/bin/env python
import os
import sys
from unipath import Path

SOURCE_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).ancestor(1)  # e.g. /home/django/source

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bhp066.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
