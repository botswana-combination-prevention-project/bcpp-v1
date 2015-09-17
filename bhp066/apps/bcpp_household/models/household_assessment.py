from django.db import models
from django.core.exceptions import ValidationError

from edc_base.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.choices import YES_NO_DONT_KNOW

from ..managers import HouseholdAssessmentManager
from ..exceptions import AlreadyReplaced

from ..choices import RESIDENT_LAST_SEEN

from .household_structure import HouseholdStructure
from .plot import Plot


class HouseholdAssessment(BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """A model completed by the user to assess a household that could not
    be enumerated."""
    household_structure = models.OneToOneField(HouseholdStructure)

    potential_eligibles = models.CharField(
        verbose_name=('Research Assistant: From speaking with the respondent, is at least one'
                      'member of this plot potentially eligible?'),
        choices=YES_NO_DONT_KNOW,
        max_length=25,
        null=True,
        editable=True,
    )

    eligibles_last_seen_home = models.CharField(
        verbose_name=('When was a resident last seen in this household?'),
        choices=RESIDENT_LAST_SEEN,
        max_length=25,
        null=True,
        blank=True,
        editable=True,
    )

    def __unicode__(self):
        return unicode(self.household_structure)

    objects = HouseholdAssessmentManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_structure.household.replaced_by:
            raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(
                self._meta.object_name, self.pk))
        if self.household_structure.enumerated:
            raise ValidationError('HouseholdStructure has been enumerated')
        if self.household_structure.failed_enumeration_attempts < 3:
            raise ValidationError('Three attempts are required before Household Assessment')
        super(HouseholdAssessment, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household_structure.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    @property
    def vdc_househould_status(self):
        return self.last_seen_home

    class Meta:
        app_label = 'bcpp_household'
        verbose_name = 'Household Residency Status Assess'
        verbose_name_plural = 'Household Residency Status Assess'
