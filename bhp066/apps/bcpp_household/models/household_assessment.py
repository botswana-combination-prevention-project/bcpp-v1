from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO, YES_NO_DONT_KNOW
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_household.managers import HouseholdAssessmentManager

from ..choices import INELIGIBLE_REASON
from ..choices import RESIDENT_LAST_SEEN
from ..constants import SEASONALLY_OCCUPIED, RARELY_OCCUPIED

from .household_structure import HouseholdStructure
from .plot import Plot


class HouseholdAssessment(BaseDispatchSyncUuidModel):

    household_structure = models.OneToOneField(HouseholdStructure)

    residency = models.CharField(
        verbose_name='Does anyone ever stay in this household?',
        choices=YES_NO,
        max_length=25,
        null=True,
        editable=True,
        )

    member_count = models.IntegerField(
        verbose_name="How many people live in this household (estimate)?",
        null=True,
        blank=True,
        help_text=("Provide the number of members in this household."))

    eligibles = models.CharField(
        verbose_name='In speaking with the individual(s) above, at least one member of this plot is potentially eligible',
        choices=YES_NO_DONT_KNOW,
        max_length=25,
        null=True,
        blank=True,
        editable=True,
        )

    ineligible_reason = models.CharField(
        verbose_name="If no members are eligible for this study, please state the reason for ineligility.",
        null=True,
        max_length=25,
        choices=INELIGIBLE_REASON,
        editable=True,
        blank=True)

    last_seen_home = models.CharField(
        verbose_name='When was a resident last seen in this household?',
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
        if self.household_structure.enumerated:
            raise ValidationError('HouseholdStructure has been enumerated')
        if self.household_structure.failed_enumeration_attempts < 3:
            raise ValidationError('Three attempts are required before Household Assessment')
        if not self.id:
            self.household_structure.failed_enumeration = True
        self.household_structure.no_informant = self.last_seen_home in [SEASONALLY_OCCUPIED, RARELY_OCCUPIED]
        self.household_structure.save()
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
