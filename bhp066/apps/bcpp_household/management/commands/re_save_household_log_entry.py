from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_household.models import HouseholdLogEntry, Household


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Re save household log entries.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        household_log_entries = HouseholdLogEntry.objects.filter(
            household_log__household_structure__household__plot__community=community_name,
            household_log__household_structure__household__replaced_by__isnull=True)
        total_entries = len(household_log_entries)
        count = 0
        for h_log_entry in household_log_entries:
            if not h_log_entry.household_log.household_structure.household.replaced_by:
                h_log_entry.save()
                count += 1
                print count, " of ", total_entries
