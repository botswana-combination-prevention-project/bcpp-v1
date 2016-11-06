from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin

from .manager_mixins import HouseholdStructureManagerMixin


class HouseholdWorkListManager(CurrentCommunityManagerMixin, HouseholdStructureManagerMixin, models.Manager):

    pass
