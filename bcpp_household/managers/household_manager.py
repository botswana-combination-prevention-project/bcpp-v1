from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class HouseholdManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = 'plot'

    def get_by_natural_key(self, household_identifier):
        return self.get(household_identifier=household_identifier)
