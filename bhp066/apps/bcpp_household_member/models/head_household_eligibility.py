from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import get_model

from edc.audit.audit_trail import AuditTrail

from apps.bcpp_household.models import BaseRepresentativeEligibility
from apps.bcpp_household.models import HouseholdStructure

from ..managers import HouseholdHeadEligibilityManager

from .household_member import HouseholdMember


class HouseholdHeadEligibility(BaseRepresentativeEligibility):
    """Determines if the household member is eligible to be treated as head of household or representative."""
    household_structure = models.ForeignKey(HouseholdStructure)

    household_member = models.OneToOneField(HouseholdMember,
        help_text=('Important: The household member must verbally consent before completing this questionnaire.'))

    objects = HouseholdHeadEligibilityManager()

    history = AuditTrail()

    def __unicode__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError("household_member cannot be None for household_head_eligibility "
                                 "with pk='\{0}\'".format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    def dispatch_container_lookup(self, using=None):
        return (get_model('bcpp_household', 'Plot'),
                'household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        self.matches_household_member_values(self.household_member)
        self.household_member.eligible_hoh = True
        self.household_member.save()
        super(HouseholdHeadEligibility, self).save(*args, **kwargs)

    def matches_household_member_values(self, household_member, exception_cls=None):
        """Compares shared values on household_member form and returns True if all match."""
        error_msg = None
        exception_cls = exception_cls or ValidationError
        if not household_member.age_in_years >= 18:
            raise exception_cls('Household member must be over 18 years of age. Got {0}.'.format(household_member.age_in_years))
        return error_msg

    class Meta:
        app_label = 'bcpp_household_member'
        unique_together = ('household_structure', 'aged_over_18', 'verbal_script')
