from django.db import models


class HouseholdAssessmentManager(models.Manager):

    def get_by_natural_key(self, household_identifier):
        Household = models.get_model('bcpp_household', 'Household')
        household = Household.objects.get_by_natural_key(household_identifier)
        return self.get(household=household)
