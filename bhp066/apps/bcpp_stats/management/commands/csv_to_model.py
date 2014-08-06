import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model


class Command(BaseCommand):

    args = '<source_path> <destination_model_name>'
    help = 'Inspect a CDC csv file and output the syntax for a basic model file'
    option_list = BaseCommand.option_list

    def strip_underscore(self, item):
        """Returns  a string stripped of a leading or tailing underscore."""
        if item.startswith('_'):
            item = item[1:]
        if item.endswith('_'):
            item = item[:-1]
        return item

    def handle(self, *args, **options):
        source_path = args[0]
        model_name = args[1]
        if get_model('bcpp_stats', model_name):
            raise CommandError('Model class {0} already exists.'.format(model_name))
        df = pd.read_csv(source_path)
        dct = df.to_dict()
        keys = dct.keys()
        keys.sort()
        attr = []
        for key in keys:
            if 'date' in key.lower():
                attr.append('{0} = models.DateField(null=True)'.format(self.strip_underscore(key)))
            else:
                attr.append('{0} = models.IntegerField(null=True)'.format(self.strip_underscore(key)))
        print """from django.db import models

from edc.core.crypto_fields.fields import EncryptedCharField

from .base_cdc import BaseCdc


class {model_name}(BaseCdc):

    {attributes}

{meta}""".format(model_name=model_name, attributes='\n    '.join(attr), meta='    class Meta:\n        app_label = \'bcpp_stats\'')
