from django.db.models import get_model

from edc.audit.audit_trail import AuditTrail

from ..managers import RepresentativeEligibilityManager

from .base_representative_eligibility import BaseRepresentativeEligibility


class RepresentativeEligibility(BaseRepresentativeEligibility):
    """Determines if the household member is eligible representative of the household."""

    objects = RepresentativeEligibilityManager()

    history = AuditTrail()

    def __unicode__(self):
        return str(self.household_structure)

    def natural_key(self):
        if not self.household_structure:
            raise AttributeError("household_structure cannot be None for representative_eligibility with pk='\{0}\'".format(self.pk))
        return self.household_structure.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure']

    def dispatch_container_lookup(self, using=None):
        return (get_model('bcpp_household', 'Plot'), 'household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_household'
