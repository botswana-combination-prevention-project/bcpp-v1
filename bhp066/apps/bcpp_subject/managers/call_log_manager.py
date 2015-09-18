from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers


class CallLogManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk, label):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member, label=label)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            return super(CallLogManager, self).get_queryset().filter(
                household_member__household_structure__household__plot__community=community)
        return super(CallLogManager, self).get_queryset()


class CallLogEntryManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk, label, call_datetime):
        CallLog = models.get_model('bcpp_subject', 'CallLog')
        call_log = CallLog.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk, label)
        return self.get(call_log=call_log, call_datetime=call_datetime)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_current_mapper().map_area
            return super(CallLogEntryManager, self).get_queryset().filter(
                call_log__household_member__household_structure__household__plot__community=community)
        return super(CallLogEntryManager, self).get_queryset()
