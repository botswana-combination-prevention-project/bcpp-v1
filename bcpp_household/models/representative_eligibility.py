from django.apps import apps as django_apps
from django.db import models

from simple_history.models import HistoricalRecords as AuditTrail

from bcpp.model_mixins import RepresentativeEligibilityMixin

from ..managers import RepresentativeEligibilityManager

from .household_structure import HouseholdStructure


class RepresentativeEligibility(RepresentativeEligibilityMixin, models.Model):
    """A model completed by the user that checks the eligibility of household member
    to be the household representative."""

    household_structure = models.OneToOneField(HouseholdStructure)

    auto_filled = models.BooleanField(
        default=False,
        editable=False,
        help_text=('This form is autofilled for non-BHS surveys using information from a'
                   'member consented in a previous survey. See HouseholdMemberHelper')
    )

    auto_fill_member_id = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='pk of household member used to autofill')

    objects = RepresentativeEligibilityManager()

    history = AuditTrail()

    def __unicode__(self):
        return str(self.household_structure)

    def natural_key(self):
        if not self.household_structure:
            raise AttributeError("household_structure cannot be None for "
                                 "representative_eligibility with pk='\{0}\'".format(self.pk))
        return self.household_structure.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure']

    def dispatch_container_lookup(self, using=None):
        return (django_apps.get_model('bcpp_household', 'Plot'), 'household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_household'
