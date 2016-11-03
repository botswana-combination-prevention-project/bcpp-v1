from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand
from django.db.models import get_model


class Command(BaseCommand):

    args = ''
    help = ('Review each household and create any missing HouseholdStructure instances.')

    def handle(self, *args, **options):
        Household = get_model('bcpp_household', 'Household')
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        HouseholdLog = get_model('bcpp_household', 'HouseholdLog')
        Survey = get_model('bcpp_survey', 'Survey')
        households = Household.objects.all()
        household_count = households.count()
        print 'Found {} households'.format(household_count)
        n = 0
        print 'Updating ...'
        for household in Household.objects.filter(plot__community__in=['ranaka', 'digawana']):
            for survey in Survey.objects.all():
                try:
                    HouseholdStructure.objects.get(household__pk=household.pk, survey=survey)
                except HouseholdStructure.DoesNotExist:
                    HouseholdStructure.objects.create(household=household, survey=survey)
                    n += 1
                except MultipleObjectsReturned:
                    print 'Did not expect {} HouseholdStructures for {} survey {}'.format(
                        HouseholdStructure.objects.filter(household__pk=household.pk, survey=survey).count(),
                        household,
                        survey)
                    for household_structure in HouseholdStructure.objects.filter(
                            household__pk=household.pk, survey=survey):
                        try:
                            HouseholdLog.objects.get(household_structure=household_structure)
                        except HouseholdLog.DoesNotExist:
                            print '   deleted for pk={}'.format(household_structure.pk)
                            household_structure.delete()
        print 'Done. Created {} HouseholdStructures.'.format(n)
