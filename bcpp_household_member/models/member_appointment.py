from django.core.urlresolvers import reverse
from django.db import models

from edc_appointment.choices import APPT_STATUS
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_constants.choices import TIME_OF_DAY, TIME_OF_WEEK

from bcpp_survey.models import Survey

from ..managers import MemberAppointmentManager

from .household_member import HouseholdMember


class MemberAppointment(BaseUuidModel):

    """A model created by the system and updated by the user for annual survey appointments."""

    household_member = models.ForeignKey(HouseholdMember)

    survey = models.ForeignKey(Survey, editable=False)

    appt_date = models.DateField(
        verbose_name=("Appointment date"),
        help_text="")

    appt_status = models.CharField(
        verbose_name=("Status"),
        choices=APPT_STATUS,
        max_length=25,
        default='new')

    label = models.CharField(
        max_length=25,
        help_text="label to group, e.g. T1 prep"
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

    is_confirmed = models.BooleanField(default=False)

    history = HistoricalRecords()

    objects = MemberAppointmentManager()

    def __str__(self):
        return '{}'.format(self.appt_date.strftime('%Y-%m-%d'))

    def natural_key(self):
        return (self.label, ) + self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.household_member', ]

    def get_report_datetime(self):
        return self.created

    def call_list(self):
        url = reverse('admin:bcpp_subject_calllist_changelist')
        return """<a href="{url}?q={q}" />call list</a>""".format(
            url=url, q=self.household_member.household_structure.pk)
    call_list.allow_tags = True

    def work_list(self):
        url = reverse('admin:bcpp_household_householdworklist_changelist')
        return """<a href="{url}?q={q}" />work list</a>""".format(
            url=url, q=self.household_member.household_structure.pk)
    work_list.allow_tags = True

    def composition(self):
        url = reverse('household_dashboard_url',
                      kwargs={'dashboard_type': 'household',
                              'dashboard_model': 'household_structure',
                              'dashboard_id': self.household_member.household_structure.pk})
        return """<a href="{url}" />{}</a>""".format(
            self.household_member.household_structure.household.household_identifier, url=url)
    composition.allow_tags = True

    class Meta:
        app_label = 'bcpp_household_member'
        unique_together = (('household_member', 'label'), )
