from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_household.utils import update_household_work_list
from bhp066.apps.bcpp_survey.models import Survey


class Command(BaseCommand):
    """ A command to update the household work list."""
    args = 'label'
    help = 'Update Household Work List'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        try:
            label = args[0]
        except IndexError:
            raise CommandError('please provide a \'label\'')
        current_survey = Survey.objects.current_survey()
        created, updated = update_household_work_list(label=label)
        print('Created {} household work list records and updated {} '
              'records for survey {}.'.format(created, updated, current_survey))
