from datetime import date

from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import date_not_future
from edc_base.model.models import BaseUuidModel

from ..choices import NEXT_APPOINTMENT_SOURCE, HOUSEHOLD_LOG_STATUS
from ..managers import HouseholdLogManager, HouseholdLogEntryManager

from .household_structure import HouseholdStructure


class HouseholdLog(BaseUuidModel):
    """A system model that links the household log to the household."""

    household_structure = models.ForeignKey(HouseholdStructure)

    objects = HouseholdLogManager()

    history = HistoricalRecords()

    def __str__(self):
        return str(self.household_structure)

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


class HouseholdLogEntry(BaseUuidModel):
    """A model completed by the user each time the household is visited."""
    household_log = models.ForeignKey(HouseholdLog)

    report_datetime = models.DateField(
        verbose_name="Report date",
        validators=[date_not_future])

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

    objects = HouseholdLogEntryManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.report_datetime, ) + self.household_log.natural_key()

    def __str__(self):
        household_log = self.household_log or None
        return '{} ({})'.format(household_log, self.report_datetime.strftime('%Y-%m-%d'))

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_log', 'report_datetime')
