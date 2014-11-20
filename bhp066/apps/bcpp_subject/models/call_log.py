from datetime import datetime

from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import datetime_is_future
from edc.choices import YES_NO_UNKNOWN, TIME_OF_DAY, TIME_OF_WEEK
from edc.device.sync.models import BaseSyncUuidModel
from edc.map.classes import site_mappers

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_survey.models.survey import Survey

from ..choices import APPT_LOCATIONS, APPT_GRADING, CONTACT_TYPE


class CallLog (BaseSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    history = AuditTrail()

    objects = models.Manager()

    def __unicode__(self):
        return '{} {} {}'.format(
            self.household_member.first_name, self.household_member.initials, self.household_member.age_in_years)

    class Meta:
        app_label = 'bcpp_subject'


class CallLogEntry (BaseSyncUuidModel):

    call_log = models.ForeignKey(CallLog)

    survey = models.ForeignKey(Survey, editable=False)

    call_datetime = models.DateTimeField(default=datetime.today())

    contact_type = models.CharField(
        max_length=15,
        choices=CONTACT_TYPE,
        help_text='If no contact made. STOP. Save form.'
    )

    has_moved_community = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the community',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        )

    new_community = models.CharField(
        max_length=50,
        verbose_name='If the participant has moved, provide the name of the community',
        help_text='',
        null=True,
        blank=True,
        )

    has_moved_community = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the household where last seen',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        )

    update_locator = models.CharField(
        max_length=7,
        verbose_name='Has the locator information changed',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        )

    available = models.CharField(
        max_length=7,
        verbose_name='Will the participant be available during the survey',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        )

    time_of_week = models.CharField(
        verbose_name='Time of week when participant will be available',
        max_length=25,
        choices=TIME_OF_WEEK,
        blank=True,
        null=True)

    time_of_day = models.CharField(
        verbose_name='Time of day when participant will be available',
        max_length=25,
        choices=TIME_OF_DAY,
        blank=True,
        null=True)

    appt = models.CharField(
        verbose_name='Is the participant willing to schedule an appointment',
        max_length=7,
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        )

    appt_date = models.DateField(
        verbose_name="Appointment Date",
        validators=[datetime_is_future],
        null=True,
        blank=True,
        )

    appt_grading = models.CharField(
        verbose_name='Is this appointment...',
        max_length=25,
        choices=APPT_GRADING,
        null=True,
        blank=True)

    appt_location = models.CharField(
        verbose_name='Appointment location',
        max_length=50,
        choices=APPT_LOCATIONS,
        null=True,
        blank=True,
        )

    appt_location_other = OtherCharField(
        verbose_name='Appointment location',
        max_length=50,
        null=True,
        blank=True,
        )

    history = AuditTrail()

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey = Survey.objects.current_survey(self.call_datetime)
        super(CallLogEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} {} {}'.format(
            self.call_log.household_member.first_name,
            self.call_log.household_member.initials,
            self.call_log.household_member.age_in_years,
            )

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ['call_log', 'call_datetime']
