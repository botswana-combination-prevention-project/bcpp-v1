from django.db import models
from django.db.models import get_model


class MemberAppointmentManager(models.Manager):

    def get_by_natural_key(self, appt_date, household_identifier, survey_name, subject_identifier_as_pk):
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(
            household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(appt_date=appt_date, household_member=household_member)
