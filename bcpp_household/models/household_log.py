from django.db import models
from edc_lib.audit_trail.audit import AuditTrail
from edc_lib.bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from edc_lib.bhp_crypto.fields import EncryptedTextField
from bcpp_household.choices import NEXT_APPOINTMENT_SOURCE, HOUSEHOLD_STATUS
from bcpp_household.managers import HouseholdLogManager, HouseholdLogEntryManager
from household_structure import HouseholdStructure
from plot import Plot
from bhp_dispatch.models import BaseDispatchSyncUuidModel


class HouseholdLog(BaseDispatchSyncUuidModel):

    household_structure = models.OneToOneField(HouseholdStructure)

    history = AuditTrail()

    objects = HouseholdLogManager()

    def __unicode__(self):
        return unicode(self.household_structure)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__plot__plot_identifier')

    def natural_key(self):
        return self.household_structure.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure', ]

    def structure(self):
        url = '/admin/{0}/householdstructure/?q={1}'.format(self._meta.app_label, self.household_structure.pk)
        return """<a href="{url}" />structure</a>""".format(url=url)
    structure.allow_tags = True

    class Meta:
        app_label = 'bcpp_household'


class HouseholdLogEntry(BaseDispatchSyncUuidModel):

    household_log = models.ForeignKey(HouseholdLog)

    report_datetime = models.DateTimeField("Report date",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    status = models.CharField(
        verbose_name='Household Status',
        max_length=25,
        default='occupied',
        choices=HOUSEHOLD_STATUS,
        editable=False,
        )
    next_appt_datetime = models.DateTimeField(
        verbose_name="Re-Visit On",
        help_text="The date and time to revisit household",
        null=True,
        blank=True
        )

    next_appt_datetime_source = models.CharField(
        verbose_name="Source",
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text='source of information for the appointment date',
        null=True,
        blank=True
        )

    comment = EncryptedTextField(
        null=True,
        blank=True,
        )

    history = AuditTrail()

    objects = HouseholdLogEntryManager()

    def natural_key(self):
        return (self.report_datetime, ) + self.household_log.natural_key()

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_log__household_structure__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_log', 'report_datetime')
