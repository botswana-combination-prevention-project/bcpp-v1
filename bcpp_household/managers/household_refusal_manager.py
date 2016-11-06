from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin

from .manager_mixins import HouseholdStructureManagerMixin


class HouseholdRefusalManager(CurrentCommunityManagerMixin, HouseholdStructureManagerMixin, models.Manager):

    pass


class HouseholdRefusalHistoryManager(CurrentCommunityManagerMixin, HouseholdStructureManagerMixin, models.Manager):

    def get_by_natural_key(self, transaction):
        return self.get(transaction=transaction)
