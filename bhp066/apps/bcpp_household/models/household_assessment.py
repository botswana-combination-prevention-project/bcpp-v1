from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO, YES_NO_DONT_KNOW
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from apps.bcpp_household.managers import HouseholdAssessmentManager

from ..choices import INELIGIBLE_REASON
from ..choices import RESIDENT_LAST_SEEN
from ..constants import RESIDENT_LAST_SEEN_4WKS, RESIDENT_LAST_SEEN_LESS_4WKS

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
        return unicode(self.household)

    objects = HouseholdAssessmentManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if not self.id:
            self.household_structure.failed_enumeration = True
        self.household_structure.no_informant = False
        if self.last_seen_home in [RESIDENT_LAST_SEEN_4WKS, RESIDENT_LAST_SEEN_LESS_4WKS]:
            self.household_structure.no_informant = True
        self.household_structure.save()
        super(HouseholdAssessment, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    @property
    def vdc_househould_status(self):
        status = None
        if self.last_seen_home == '4_weeks_a_year':
            status = 'seasonally_occupied'
        elif self.last_seen_home == '1_night_less_than_4_weeks_year':
            status = 'rarely_occupied'
        elif self.last_seen_home == 'never_spent_1_day_over_a_year':
            status = 'never_occupied'
        return status

    class Meta:
        app_label = 'bcpp_household'
        verbose_name = 'Household Residency Status Assess'
        verbose_name_plural = 'Household Residency Status Assess'
