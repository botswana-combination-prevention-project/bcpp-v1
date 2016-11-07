from django.apps import apps as django_apps
from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class HouseholdMemberManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['household_structure', 'household', 'plot']

    def get_by_natural_key(self, household_identifier, survey_name, subject_identifier_as_pk):
        HouseholdStructure = django_apps.get_model('bcpp_household', 'HouseholdStructure')
        RegisteredSubject = django_apps.get_model('registration', 'RegisteredSubject')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(household_structure=household_structure, registered_subject=registered_subject)
