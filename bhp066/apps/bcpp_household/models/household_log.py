from django.db import models
from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_before_study_start, date_not_future
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.core.crypto_fields.fields import EncryptedTextField
from ..choices import YES_NO
from apps.bcpp_survey.validators import date_in_survey
from apps.bcpp_household_member.models import HouseholdMember
from ..choices import NEXT_APPOINTMENT_SOURCE, HOUSEHOLD_STATUS
from ..managers import HouseholdLogManager, HouseholdLogEntryManager
from .household_structure import HouseholdStructure
from .plot import Plot


class HouseholdLog(BaseDispatchSyncUuidModel):
    #Household
    household_structure = models.OneToOneField(HouseholdStructure)

    history = AuditTrail()

    objects = HouseholdLogManager()

    def __unicode__(self):
        return unicode(self.household_structure)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

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

    report_datetime = models.DateField("Report date",
        validators=[date_not_before_study_start, date_not_future],
        )

    household_status = models.CharField(
        verbose_name='Household Status',
        max_length=50,
        choices=HOUSEHOLD_STATUS,
        null=True,
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

    def save(self, *args, **kwargs):
        household = self.household_log.household_structure.household
        if self.household_status:
            household.household_status = self.household_status
        household.save()

        super(HouseholdLogEntry, self).save(*args, **kwargs)

    def bypass_for_edit_dispatched_as_item(self):
        return True

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_log__household_structure__household__plot__plot_identifier')

    def __unicode__(self):
        return unicode(self.household_log) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_log', 'report_datetime')
