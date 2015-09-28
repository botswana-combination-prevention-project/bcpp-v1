from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_household.models import HouseholdLog


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Re save household log entries.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        household_log_entries = HouseholdLog.objects.filter(
            household_log__household_structure__household__plot__community=community_name)
        total_entries = len(household_log_entries)
        count = 0
        for h_log_entries in household_log_entries:
            h_log_entries.save()
            count += 1
            print count, " of ", total_entries
