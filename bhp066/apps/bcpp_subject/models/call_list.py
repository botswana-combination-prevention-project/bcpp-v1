from dateutil.relativedelta import relativedelta

from django.core.urlresolvers import reverse
from django.db import models

from edc.choices.common import GENDER
from edc.device.sync.models import BaseSyncUuidModel
from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import FirstnameField
from edc_base.model.validators import datetime_not_future, datetime_not_before_study_start
from edc_constants.constants import CLOSED, OPEN, NEW

from bhp066.apps.bcpp_household_member.models import HouseholdMember, MemberAppointment

from ..choices import REFERRAL_CODES
from ..managers import CallListManager

from .subject_consent import SubjectConsent


class CallList (BaseSyncUuidModel):

    CONSENT_MODEL = SubjectConsent

    household_member = models.ForeignKey(HouseholdMember)

    community = models.CharField(
        max_length=50)

    subject_identifier = models.CharField(
        max_length=25)

    call_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='last call datetime updated by call log entry',
    )

    app_label = models.CharField(
        max_length=25,
        editable=False)

    object_name = models.CharField(
        max_length=25,
        editable=False)

    object_pk = models.CharField(
        max_length=50,
        editable=False)

    first_name = FirstnameField(
        verbose_name='First name',
        editable=False,
    )

    initials = models.CharField(
        verbose_name='Initials',
        max_length=3,
        editable=False,
    )

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER,
        editable=False,
    )

    age_in_years = models.IntegerField(
        verbose_name='Age in years',
        null=True,
        editable=False,
    )

    bhs = models.BooleanField(default=False)

    consent_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text="From Subject Consent."
    )

    referral_code = models.CharField(
        verbose_name='Referral Code',
        max_length=50,
        choices=REFERRAL_CODES,
        editable=False,
        null=True,
        help_text="updated from subject referral"
    )

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        null=True,
        help_text="From Subject Consent."
    )

    hic = models.BooleanField(default=False)

    hic_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        null=True,
        help_text="From HIC Enrollment.report_datetime."
    )

    call_attempts = models.IntegerField(
        default=0)

    call_outcome = models.TextField(
        max_length=150,
        null=True,
    )

    call_status = models.CharField(
        max_length=15,
        choices=(
            (NEW, 'New'),
            (OPEN, 'Open'),
            (CLOSED, 'Closed'),
        ),
        default=NEW,
    )

    label = models.CharField(
        max_length=25,
        null=True,
        help_text="label to group reasons for contact, e.g. T1 preparation"
    )

    member_appointment = models.ForeignKey(MemberAppointment, null=True, editable=False)

    history = AuditTrail()

    objects = CallListManager()

    def __unicode__(self):
        return '{} {} {} {} ({} call)'.format(
            self.subject_identifier,
            self.household_member.first_name,
            self.household_member.initials,
            self.household_member.household_structure.survey,
            self.label,
        )

    def age(self):
        return relativedelta(self.consent_datetime.date(), self.dob).years
    age.allow_tags = True

    def composition(self):
        url = reverse('household_dashboard_url', kwargs={
            'dashboard_type': 'household',
            'dashboard_model': 'household_structure',
            'dashboard_id': self.household_member.household_structure.pk
        })
        return '<a href="{}">{}</A>'.format(
            url, self.household_member.household_structure.household.household_identifier)
    composition.allow_tags = True

    def appt(self):
        if self.member_appointment:
            url = reverse('admin:bcpp_household_member_memberappointment_changelist')
            return '<a href="{0}?q={1}">{2}</A>'.format(
                url, self.household_member.household_structure.pk, unicode(self.member_appointment))
        return ''
    appt.allow_tags = True

    def work_list(self):
        url = reverse('admin:bcpp_household_householdworklist_changelist')
        return """<a href="{url}?q={q}" />work list</a>""".format(
            url=url, q=self.household_member.household_structure.pk)
    work_list.allow_tags = True

    def natural_key(self):
        return self.household_member.natural_key() + (self.label, )
    natural_key.dependencies = ['bcpp_household_member.household_member', ]

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ['household_member', 'label']
