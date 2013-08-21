from django.db import models
from bhp_base_model.validators import (datetime_not_before_study_start, datetime_not_future,
                                       dob_not_future, MinConsentAge, MaxConsentAge)
from bhp_base_model.fields import IsDateEstimatedField
from bcpp_household_member.models import HouseholdMember
from bhp_registration.models import RegisteredSubject
from bhp_appointment_helper.models import BaseAppointmentMixin
from bhp_botswana.models import BaseBwConsent
from bhp_botswana.fields import EncryptedOmangField
from audit_trail.audit import AuditTrail
from bcpp.choices import COMMUNITIES
from bcpp_subject.choices import COUNSELING_SITE
from bhp_common.choices import GENDER_UNDETERMINED, YES_NO, YES_NO_DONT_KNOW


class HtcRegistration (BaseAppointmentMixin, BaseBwConsent):

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
    
#Inherited already from base class
#     dob = models.DateField(
#         verbose_name="Date of birth",
#         validators=[
#             dob_not_future,
#             MinConsentAge,
#             MaxConsentAge,
#             ],
#         null=True,
#         blank=False,
#         help_text="Format is YYYY-MM-DD.",
#         )
# 
#     is_dob_estimated = IsDateEstimatedField(
#         verbose_name="Is date of birth estimated?",
#         null=True,
#         blank=False,
#         )
# 
#     gender = models.CharField(
#         verbose_name="Gender",
#         choices=GENDER_UNDETERMINED,
#         max_length=1,
#         null=True,
#         blank=False,
#         )
# 
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
        app_label = "bcpp_htc"
        verbose_name = "HTC registration"
        verbose_name_plural = "HTC Registration"
