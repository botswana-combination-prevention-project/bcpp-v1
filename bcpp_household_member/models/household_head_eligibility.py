from django.core.exceptions import ValidationError
from django.db import models

from edc_base.model.models import HistoricalRecords

from bcpp.model_mixins import RepresentativeEligibilityMixin
from bcpp_household.models import HouseholdStructure

from ..managers import HouseholdMemberManagerMixin

from .model_mixins import HouseholdMemberModelMixin


class HouseholdHeadEligibility(RepresentativeEligibilityMixin, HouseholdMemberModelMixin):
    """A model completed by the user that determines if the household member is eligible to act
    as a head of household or household representative."""
    household_structure = models.ForeignKey(HouseholdStructure)

    objects = HouseholdMemberManagerMixin()

    history = HistoricalRecords()

    def __str__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError("household_member cannot be None for "
                                 "household_head_eligibility "
                                 "with pk='\{0}\'".format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    def save(self, *args, **kwargs):
        self.matches_household_member_values(self.household_member)
        super(HouseholdHeadEligibility, self).save(*args, **kwargs)

    def matches_household_member_values(self, household_member, exception_cls=None):
        """Compares shared values on household_member form and
        returns True if all match."""
        error_msg = None
        exception_cls = exception_cls or ValidationError
        if not household_member.age_in_years >= 18:
            raise exception_cls('Household member must be over 18 years of age. '
                                'Got {0}.'.format(household_member.age_in_years))
        return error_msg

    class Meta:
        app_label = 'bcpp_household_member'
        unique_together = ('household_structure', 'aged_over_18', 'verbal_script')
