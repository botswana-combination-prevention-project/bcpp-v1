from django.db import models


class CallLogManager(models.Manager):
    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk, label):
        HouseholdMember = models.get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member, label=label)


class CallLogEntryManager(models.Manager):
    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk, label, call_datetime):
        CallLog = models.get_model('bcpp_subject', 'CallLog')
        call_log = CallLog.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk, label)
        return self.get(call_log=call_log, call_datetime=call_datetime)