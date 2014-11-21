from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.choices.common import GENDER
from edc.core.crypto_fields.fields import EncryptedFirstnameField
from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future, datetime_not_before_study_start
from edc.constants import CLOSED, OPEN, NEW
from edc.device.sync.models import BaseSyncUuidModel

from apps.bcpp_household_member.models import HouseholdMember

from ..choices import REFERRAL_CODES


class CallList (BaseSyncUuidModel):

    household_member = models.ForeignKey(HouseholdMember)

    community = models.CharField(
        max_length=50)

    subject_identifier = models.CharField(
        max_length=25)

    app_label = models.CharField(
        max_length=25,
        editable=False)

    object_name = models.CharField(
        max_length=25,
        editable=False)

    object_pk = models.CharField(
        max_length=50,
        editable=False)

    first_name = EncryptedFirstnameField(
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
        verbose_name=_('Age in years'),
        null=True,
        editable=False,
        )

    bhs = models.BooleanField(default=False)

    consent_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text=_("From Subject Consent.")
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
        help_text=_("From Subject Consent.")
        )

    hic = models.BooleanField(default=False)

    hic_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        null=True,
        help_text=_("From HIC Enrollment.report_datetime.")
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

    history = AuditTrail()

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

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ['household_member', 'label']
