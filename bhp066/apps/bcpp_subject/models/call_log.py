from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField
from edc_base.encrypted_fields import EncryptedTextField
from edc_base.model.validators import date_is_future
from edc.choices import YES_NO_UNKNOWN, TIME_OF_DAY, TIME_OF_WEEK, ALIVE_DEAD_UNKNOWN, YES_NO
from edc_constants.constants import YES, NO, DEAD
from edc.device.sync.models import BaseSyncUuidModel

from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models.survey import Survey

from ..choices import APPT_LOCATIONS, APPT_GRADING, CONTACT_TYPE
from ..managers import CallLogEntryManager, CallLogManager
from ..validators import date_in_survey

from .subject_locator import SubjectLocator


class CallLog (BaseSyncUuidModel):

    household_member = models.ForeignKey(HouseholdMember)

    survey = models.ForeignKey(Survey, editable=False)

    locator_information = EncryptedTextField(
        help_text='This information has been imported from the previous locator. You may update as required.')

    contact_notes = EncryptedTextField(
        null=True,
        blank=True,
        help_text='')

    label = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        help_text="from call list")

    history = AuditTrail()

    objects = CallLogManager()

    def __unicode__(self):
        return '{} {} {} ({} call)'.format(
            self.household_member.first_name,
            self.household_member.initials,
            self.household_member.household_structure.survey.survey_name,
            self.label)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', [])
        if not self.survey:
            self.survey = Survey.objects.current_survey(datetime.today())
        if 'locator_information' in update_fields or not self.locator_information:
            try:
                self.locator_information = SubjectLocator.objects.previous(
                    self.household_member).formatted_contact_information
            except AttributeError as err_message:
                self.locator_information = str(err_message)
        super(CallLog, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household_member.natural_key() + (self.label, )
    natural_key.dependencies = ['bcpp_household_member.household_member', ]

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ['household_member', 'label']


class CallLogEntry (BaseSyncUuidModel):

    call_log = models.ForeignKey(CallLog)

    survey = models.ForeignKey(Survey, editable=False)

    call_datetime = models.DateTimeField()

    invalid_numbers = models.CharField(
        verbose_name='Indicate any invalid numbers dialed from the locator information above?',
        max_length=50,
        validators=[RegexValidator(
            regex=r'^[0-9]{7,8}(,[0-9]{7,8})*$',
            message='Only enter contact numbers separated by commas. No spaces and no trailing comma.'), ],
        null=True,
        blank=True,
        help_text='Separate by comma (,).'
    )

    contact_type = models.CharField(
        max_length=15,
        choices=CONTACT_TYPE,
        help_text='If no contact made. STOP. Save form.'
    )

    survival_status = models.CharField(
        verbose_name='Survival status of the participant',
        max_length=10,
        choices=ALIVE_DEAD_UNKNOWN,
        help_text=""
    )

    update_locator = models.CharField(
        max_length=7,
        verbose_name='Has the locator information changed',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        help_text=('If YES, please enter the changed information '
                   'in the box above entitled (2) Locator information')
    )

    moved_community = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the community',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        help_text=""
    )

    new_community = models.CharField(
        max_length=50,
        verbose_name='If the participant has moved, provide the name of the new community',
        null=True,
        blank=True,
        help_text="If moved out of the community, provide a new community name or \'UNKNOWN\'"
    )

    moved_household = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the household where last seen',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        help_text=""
    )

    available = models.CharField(
        max_length=7,
        verbose_name='Will the participant be available during the survey',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        help_text=""
    )

    time_of_week = models.CharField(
        verbose_name='Time of week when participant will be available',
        max_length=25,
        choices=TIME_OF_WEEK,
        blank=True,
        null=True,
        help_text=""
    )

    time_of_day = models.CharField(
        verbose_name='Time of day when participant will be available',
        max_length=25,
        choices=TIME_OF_DAY,
        blank=True,
        null=True,
        help_text=""
    )

    appt = models.CharField(
        verbose_name='Is the participant willing to schedule an appointment',
        max_length=7,
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=True,
        help_text=""
    )

    appt_date = models.DateField(
        verbose_name="Appointment Date",
        validators=[date_is_future, date_in_survey],
        null=True,
        blank=True,
        help_text="This can only come from the participant."
    )

    appt_grading = models.CharField(
        verbose_name='Is this appointment...',
        max_length=25,
        choices=APPT_GRADING,
        null=True,
        blank=True,
        help_text=""
    )

    appt_location = models.CharField(
        verbose_name='Appointment location',
        max_length=50,
        choices=APPT_LOCATIONS,
        null=True,
        blank=True,
        help_text=""
    )

    appt_location_other = OtherCharField(
        verbose_name='Appointment location',
        max_length=50,
        null=True,
        blank=True,
        help_text=""
    )

    call_again = models.CharField(
        verbose_name='Call the participant again?',
        max_length=10,
        choices=YES_NO,
        default=YES,
        help_text=''
    )

    history = AuditTrail()

    objects = CallLogEntryManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey = Survey.objects.current_survey(self.call_datetime)
        if self.survival_status == DEAD:
            self.call_again = NO
        super(CallLogEntry, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} {} {}'.format(
            self.call_log.household_member.first_name,
            self.call_log.household_member.initials,
            self.call_log.household_member.age_in_years,
        )

    def natural_key(self):
        return self.call_log.natural_key() + (self.call_datetime, )

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ['call_log', 'call_datetime']
