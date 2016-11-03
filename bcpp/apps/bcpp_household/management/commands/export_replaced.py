import csv
from datetime import datetime
import os

from django.core.management.base import BaseCommand

from bhp066.apps.bcpp_household.models import Plot, Household


class Command(BaseCommand):
    """ A command to export to csv plots and households affected by plot replacement."""
    args = ''
    help = 'Export replaced plots and households.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        header = ['model', 'identifier', 'replaces', 'replaced_by', 'action', 'status', 'selected', 'bhs', 'htc']
        date_suffix = datetime.today().strftime('%Y%m%d%H%M')
        with open(os.path.join(os.path.expanduser('~/plot_replacement_{}.csv').format(date_suffix)), 'w') as f:
            writer = csv.writer(f,)
            if header:
                writer.writerow(header)
                header = []
            plots = [
                [p.plot_identifier, p.replaces, p.replaced_by, p.action, p.status,
                 p.selected, p.bhs, p.htc] for p in Plot.objects.filter(replaces__isnull=False)]
            for tpl in plots:
                writer.writerow(['plots (replaces)'] + tpl)
            plots = [
                [p.plot_identifier, p.replaces, p.replaced_by, p.action, p.status, p.selected,
                 p.bhs, p.htc] for p in Plot.objects.filter(replaced_by__isnull=False)]
            for tpl in plots:
                writer.writerow(['plots (replaced_by)'] + tpl)
            households = [
                [h.household_identifier, h.plot.replaces, h.replaced_by, h.plot.action,
                 h.plot.status, h.plot.selected, h.plot.bhs, h.plot.htc
                 ] for h in Household.objects.filter(replaced_by__isnull=False)]
            for tpl in households:
                writer.writerow(['households (replaced_by)'] + tpl)
        print ('~/plot_replacement_{}.csv').format(date_suffix)
