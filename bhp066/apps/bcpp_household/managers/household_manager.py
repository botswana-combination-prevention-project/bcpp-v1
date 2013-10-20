from django.db import models


class HouseholdManager(models.Manager):

    def get_by_natural_key(self, household_identifier):
        return self.get(household_identifier=household_identifier)
