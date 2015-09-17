from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.base.model.fields.local.bw import EncryptedOmangField
from edc.base.model.validators import (datetime_not_before_study_start, datetime_not_future)
from edc.choices.common import YES_NO, YES_NO_DONT_KNOW
from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.choices import COUNSELING_SITE


class HtcRegistration (BaseAppointmentMixin):

    household_member = models.OneToOneField(HouseholdMember)

    registered_subject = models.OneToOneField(RegisteredSubject)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date/Time",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    is_resident = models.CharField(
        verbose_name="Is this your community of residence?",
        choices=YES_NO,
        max_length=3,
        help_text="Community of residence is where an individual spends on average >=14 nights per month",
        )

    your_community = models.CharField(
        verbose_name="What is your community of residence?",
        max_length=50,
        choices=COMMUNITIES,
        null=True,
        blank=True,
        )

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    omang = EncryptedOmangField(
        verbose_name="Identity number (OMANG, etc)",
        unique=True,
        help_text="Use Omang, Passport number, driver's license number or Omang receipt number"
        )

#Does Tebelopele have these as per new protocol? They need to update their form
#     legal_marriage = models.CharField(
#         verbose_name=("If not a citizen, are you legally married to a Botswana Citizen?"),
#         max_length=3,
#         choices=YES_NO,
#         null=True,
#         blank=True,
#         validators=[eligible_if_yes, ],
#         help_text=" if 'NO,' STOP participant cannot be enrolled",
#         )
#
#     marriage_certificate = models.CharField(
#         verbose_name=("Has the participant produced the marriage certificate, as proof? "),
#         max_length=3,
#         choices=YES_NO,
#         null=True,
#         blank=True,
#         validators=[eligible_if_yes, ],
#         help_text=" if 'NO,' STOP participant cannot be enrolled",
#         )
#
#     marriage_certificate_no = models.CharField(
#         verbose_name=("What is the marriage certificate number?"),
#         max_length=9,
#         null=True,
#         blank=True,
#         help_text="e.g. 000/YYYY",
#         )
    is_pregnant = models.CharField(
        verbose_name=("Are you pregnant?"),
        max_length=15,
        choices=YES_NO_DONT_KNOW,
        null=True,
        blank=True,
        help_text=" For female participants only",
        )

    testing_counseling_site = models.CharField(
        verbose_name=("Testing and Counseling Site"),
        max_length=15,
        choices=COUNSELING_SITE,
        null=True,
        blank=True,
        help_text="",
        )

    history = AuditTrail()

    def get_registration_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = "bcpp_htc_subject"
        verbose_name = "HTC registration"
        verbose_name_plural = "HTC Registration"
