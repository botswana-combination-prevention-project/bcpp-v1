from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers


class CallListManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk, label):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member, label=label)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(CallListManager, self).get_queryset().filter(
                household_member__household_structure__household__plot__community=community)
        return super(CallListManager, self).get_queryset()
