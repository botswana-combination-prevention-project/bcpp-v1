from django.apps import apps as django_apps


class HouseholdStructureManagerMixin:

    def get_by_natural_key(self, household_identifier, survey_name):
        HouseholdStructure = django_apps.get_model('bcpp_household', 'HouseholdStructure')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        return self.get(household_structure=household_structure)
