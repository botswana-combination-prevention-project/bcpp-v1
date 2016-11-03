import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from ...utils import strip_underscore


class Command(BaseCommand):
    """A Management command that generates the syntax for a model file based on a given CSV file."""
    args = '<source_path> <destination_model_name>'
    help = 'Inspect a CDC csv file and output the syntax for a basic model file'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        """Prints model syntax  based on the given CSV file.

        All fields are assumed to be IntegerFields unless the column name
        has the word 'date' in it. Some manual editing of the proposed model
        syntax will be necessary.

        Usage: python manage.py csv_to_model <source_path> <destination_model_name>."""
        source_path = args[0]
        model_name = args[1]
        if get_model('bcpp_stats', model_name):
            raise CommandError('Model class {0} already exists.'.format(model_name))
        keys = pd.read_csv(source_path).to_dict().keys()
        keys.sort()
        attr = []
        for key in keys:
            if 'date' in key.lower():
                attr.append('{0} = models.DateField(null=True)'.format(strip_underscore(key)))
            else:
                attr.append('{0} = models.IntegerField(null=True)'.format(strip_underscore(key)))
        print """from django.db import models

from edc.core.crypto_fields.fields import EncryptedIdentityField

from .base_cdc import BaseCdc


class {model_name}(BaseCdc):

    {attributes}

{meta}""".format(model_name=model_name,
                 attributes='\n    '.join(attr), meta='    class Meta:\n        app_label = \'bcpp_stats\'')
