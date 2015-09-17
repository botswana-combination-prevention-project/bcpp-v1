from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.choices import TIME_OF_DAY, TIME_OF_WEEK
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.appointment.choices import APPT_STATUS

from bhp066.apps.bcpp_survey.models import Survey

from ..managers import MemberAppointmentManager

from .household_member import HouseholdMember


class MemberAppointment(BaseDispatchSyncUuidModel):

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

    history = AuditTrail()

    objects = MemberAppointmentManager()

    def __unicode__(self):
        return '{}'.format(self.appt_date.strftime('%Y-%m-%d'))

    def natural_key(self):
        return (self.label, ) + self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.household_member', ]

    def get_report_datetime(self):
        return self.created

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_member__household_structure__household__plot')

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
