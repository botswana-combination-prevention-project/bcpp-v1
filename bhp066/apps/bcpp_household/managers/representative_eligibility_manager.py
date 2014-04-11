from django.db import models
from django.db.models import get_model


class RepresentativeEligibilityManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        return self.get(household_structure=household_structure)
