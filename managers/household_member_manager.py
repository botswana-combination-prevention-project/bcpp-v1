from django.db import models
from django.db.models import get_model


class HouseholdStructureMemberManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk):
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        RegisteredSubject = get_model('bhp_registration', 'RegisteredSubject')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(household_structure=household_structure, registered_subject=registered_subject)
