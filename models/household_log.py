from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bhp_crypto.fields import EncryptedCharField
from bcpp_household.choices import NEXT_APPOINTMENT_SOURCE
from bcpp_survey.models import Survey
from bcpp_household.managers import HouseholdLogManager, HouseholdLogEntryManager
from household import Household
from base_uuid_model import BaseUuidModel


class HouseholdLog(BaseUuidModel):

    household = models.ForeignKey(Household)

    survey = models.ForeignKey(Survey)

    history = AuditTrail()

    objects = HouseholdLogManager()

    def __unicode__(self):
        return '{0}-{1}'.format(self.household, self.survey)

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household__household_identifier')

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_survey.survey', 'bcpp_household.household', ]

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household', 'survey')


class HouseholdLogEntry(BaseUuidModel):

    household_log = models.ForeignKey(HouseholdLog)

    report_datetime = models.DateTimeField("Report date",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    hbc = models.CharField(
        verbose_name='HBC/CLO Name',
        max_length=25,
        )

    next_appt_datetime = models.DateTimeField(
        verbose_name="Re-Visit On",
        help_text="The date and time to revisit household",
        null=True,
        blank=False
        )

    next_appt_datetime_source = models.CharField(
        verbose_name="Source",
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text='',
        null=True,
        blank=False
        )

#     rcc_collection_date = models.DateField(
#         verbose_name='Collect RCC On',
#         null=True,
#         blank=True)
# 
#     rcc_collected = models.BooleanField(default=False)

    comment = EncryptedCharField(
        null=True,
        blank=True,
        )

    history = AuditTrail()

    objects = HouseholdLogEntryManager()

    def natural_key(self):
        return (self.report_datetime, ) + self.household_log.natural_key()

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household_log__household__household_identifier')

    class Meta:
        app_label = 'bcpp_household'
        unique_together = ('household_log', 'report_datetime')
