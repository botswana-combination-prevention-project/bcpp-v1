from django.db import models
from django.db.models import get_model


class EnrollmentLossManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk):
        #Loss form is OneToOne with household_member
        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(household_identifier, survey_name, subject_identifier_as_pk)
        return self.get(household_member=household_member)
