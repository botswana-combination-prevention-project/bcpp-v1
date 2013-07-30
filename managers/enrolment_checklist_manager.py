from django.db import models
from django.db.models import get_model


class EnrolmentChecklistManager(models.Manager):

    def get_by_natural_key(self, household_structure):
        HouseholdMember = get_model('bcpp_household', 'HouseholdMember')
        household_member = HouseholdMember.objects.get_by_natural_key(household_structure)
        return self.get(household_member=household_member)
