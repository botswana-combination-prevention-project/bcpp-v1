from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin

from .manager_mixins import HouseholdStructureManagerMixin


class HouseholdAssessmentManager(CurrentCommunityManagerMixin, HouseholdStructureManagerMixin, models.Manager):

    pass
