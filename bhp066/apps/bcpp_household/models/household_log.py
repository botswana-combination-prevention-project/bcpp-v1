from datetime import date

from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.validators import date_not_before_study_start, date_not_future
from edc_base.model.models import BaseUuidModel
from edc_base.encrypted_fields import EncryptedTextField
from edc.device.sync.models import BaseSyncUuidModel
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from ..choices import NEXT_APPOINTMENT_SOURCE, HOUSEHOLD_LOG_STATUS
from ..managers import HouseholdLogManager, HouseholdLogEntryManager
from ..exceptions import AlreadyReplaced

from .household_structure import HouseholdStructure
from .plot import Plot


class HouseholdLog(BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """A system model that links the household log to the household."""
    household_structure = models.ForeignKey(HouseholdStructure)

    history = AuditTrail()

    objects = HouseholdLogManager()

    def __unicode__(self):
        return unicode(self.household_structure)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    def natural_key(self):
        return self.household_structure.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure', ]

    @property
    def todays_household_log_entries(self):
        """Confirms there is an househol_log_entry for today."""
        today = date.today()
        return HouseholdLogEntry.objects.filter(
            household_log=self,
            report_datetime__year=today.year,
            report_datetime__month=today.month,
            report_datetime__day=today.day)

    def structure(self):
        url = '/admin/{0}/householdstructure/?q={1}'.format(self._meta.app_label, self.household_structure.pk)
        return """<a href="{url}" />structure</a>""".format(url=url)
    structure.allow_tags = True

    def deserialize_prep(self, **kwargs):
        # HouseholdLog being deleted by an IncommingTransaction, we go ahead and delete it.
        # An extra household created by mistake.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = 'bcpp_household'


class HouseholdLogEntry(BaseDispatchSyncUuidModel, BaseUuidModel):
    """A model completed by the user each time the household is visited."""
    household_log = models.ForeignKey(HouseholdLog)

    report_datetime = models.DateField(
        verbose_name="Report date",
        validators=[date_not_before_study_start, date_not_future])

    household_status = models.CharField(
        verbose_name='Household Status',
        max_length=50,
        choices=HOUSEHOLD_LOG_STATUS,
        null=True,
        blank=False)

    next_appt_datetime = models.DateTimeField(
        verbose_name="Re-Visit On",
        help_text="The date and time to revisit household",
        null=True,
        blank=True)

    next_appt_datetime_source = models.CharField(
        verbose_name="Source",
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text='source of information for the appointment date',
        null=True,
        blank=True)

    comment = EncryptedTextField(
        null=True,
        blank=True)

    history = AuditTrail()

    objects = HouseholdLogEntryManager()

    def natural_key(self):
        return (self.report_datetime, ) + self.household_log.natural_key()

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(
            household_identifier=self.household_log.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
        super(HouseholdLogEntry, self).save(*args, **kwargs)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_log__household_structure__household__plot__plot_identifier')

    def __unicode__(self):
        household_log = self.household_log or None
        return unicode(household_log) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_log', 'report_datetime')
