import csv
from datetime import datetime
import os

from django.core.management.base import BaseCommand

from edc.map.classes import site_mappers

from edc.base.model.fields.helpers.revision import site_revision


class Command(BaseCommand):
    """ A command to export mapper data as a wiki table."""
    args = 'community'
    help = 'Export mapper data as a wiki table.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        site_mappers.sort_by_code()
        body = []
        header = []
        for mapper in site_mappers:
            if mapper.map_code not in ['00', '01']:
                for item, values in mapper().survey_dates.iteritems():
                    body.append('|{}||{}||{}'.format(
                        str(mapper()),
                        item,
                        '{}'.format('||'.join([str(getattr(values, f)) for f in values._fields]))))
                    if not header:
                        header = [f for f in values._fields]
        header = ['Community', 'Survey'] + header
        print('{| class="wikitable sortable"\n')
        print('!{}\n|-\n'.format('!!'.join(header)))
        print('\n|-\n'.join(body))
        print('\n|}\n')
        print('\nBHP066 Edc {} ({})\n'.format(site_revision.tag, site_revision.branch))
