from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class HouseholdMemberManagerMixin(CurrentCommunityManagerMixin, models.Manager):
    """Manager base class for managers on models with key to HouseholdMember."""

    lookup = ['household_member', 'household_structure', 'household', 'plot']

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk):
        HouseholdMember = django_apps.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member)
