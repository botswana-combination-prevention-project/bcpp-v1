from django.db import models
from django.utils.translation import ugettext as _
from bhp_base_model.validators import (datetime_not_before_study_start, datetime_not_future,
                                       dob_not_future, MinConsentAge, MaxConsentAge)
from bhp_base_model.fields import IsDateEstimatedField
from household_member import HouseholdMember
from bhp_registration.models import RegisteredSubject
from bhp_dispatch.models import BaseDispatchSyncUuidModel
from bhp_botswana.fields import EncryptedOmangField
from bhp_base_model.fields import OtherCharField
from audit_trail.audit import AuditTrail
from bcpp_list.models import Religion
from bhp_common.choices import POS_NEG_ONLY, GENDER_UNDETERMINED, YES_NO
from bcpp.choices import ETHNIC_CHOICE, MARITALSTATUS_CHOICE, WHYNOHIVTESTING_CHOICE


class HtcData (BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    registered_subject = models.OneToOneField(RegisteredSubject)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date/Time",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[
            dob_not_future,
            MinConsentAge,
            MaxConsentAge,
            ],
        null=True,
        blank=False,
        help_text="Format is YYYY-MM-DD. (Data will not be saved if ineligible)",
        )

    is_dob_estimated = IsDateEstimatedField(
        verbose_name="Is date of birth estimated?",
        null=True,
        blank=False,
        )

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_UNDETERMINED,
        max_length=1,
        null=True,
        blank=False,
        )

    omang = EncryptedOmangField(
        verbose_name="Identity number (OMANG, etc)",
        unique=True,
        help_text="Use Omang, Passport number, driver's license number or Omang receipt number (Data will not be saved if ineligible)"
        )

    citizen = models.CharField(
        verbose_name="[Interviewer] Is the prospective participant a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
#         validators=[eligible_if_yes, ],
        help_text="",
        )

    rel = models.ManyToManyField(Religion,
        verbose_name=_("What is your religion affiliation?"),
        help_text="",
        )
    rel_other = OtherCharField()

    ethnic = models.CharField(
        verbose_name=_("What is your ethnic group?"),
        max_length=35,
        choices=ETHNIC_CHOICE,
        help_text="Ask for the original ethnic group",
        )
    other = OtherCharField()

    marital_status = models.CharField(
        verbose_name=_("What is your current marital status?"),
        max_length=55,
        choices=MARITALSTATUS_CHOICE,
        help_text="",
        )
    num_wives = models.IntegerField(
        verbose_name=_("How many wives does your husband have (including traditional marriage),"
                        " including yourself?"),
        max_length=2,
        null=True,
        blank=True,
        help_text="Leave blank if participant does not want to respond.",
        )
    husband_wives = models.IntegerField(
        verbose_name=_("How many wives do you have, including traditional marriage?"),
        max_length=2,
        null=True,
        blank=True,
        help_text="Leave blank if participant does not want to respond.",
        )

    hiv_result = models.CharField(
        verbose_name=_("Record today\'s HIV test result:"),
        max_length=50,
        choices=POS_NEG_ONLY,
        help_text="",
        )

    why_not_tested = models.CharField(
        verbose_name=_("What was the main reason why you did not want HIV testing"
                       " as part of today's visit?"),
        max_length=65,
        null=True,
        blank=True,
        choices=WHYNOHIVTESTING_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
        )

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "HTC Data"
        verbose_name_plural = "HTC Data"
