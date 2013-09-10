from uuid import uuid4
from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.validators import eligible_if_yes, eligible_if_no
from bhp_common.choices import YES_NO, YES_NO_REFUSED
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bhp_dispatch.models import BaseDispatchSyncUuidModel
from bhp_registration.models import RegisteredSubject
from bhp_crypto.fields import EncryptedCharField
from bhp_botswana.fields import EncryptedOmangField
from bhp_base_model.fields import IsDateEstimatedField
from bhp_base_model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from bhp_common.choices import GENDER_UNDETERMINED
from household_member import HouseholdMember
from bcpp_household.models import Household
from bcpp_household_member.managers import EnrolmentChecklistManager


class EnrolmentChecklist (BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    registered_subject = models.OneToOneField(RegisteredSubject)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date/Time",
        validators=[datetime_not_before_study_start, datetime_not_future],
        )

    eligible = models.BooleanField(default=False, editable=False)

    reason_not_eligible = EncryptedCharField(null=True, editable=False)

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
    
    legal_marriage = models.CharField(
        verbose_name=("If not a citizen, are you legally married to a Botswana Citizen?"),
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )
 
    marriage_certificate = models.CharField(
        verbose_name=("Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )
    
    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY",
        )

    community_resident = models.CharField(
        verbose_name=("[Participant] In the past 12 months, have you typically spent 3 or"
                      " more nights per month in [name of study community]? [If moved into the"
                      " community in the past 12 months, then since moving in have you typically"
                      " spent more than 3 nights per month in this community] "),
        max_length=17,
        choices=YES_NO_REFUSED,
        validators=[eligible_if_yes, ],
        help_text="if 'NO (or don't want to answer)' STOP participant cannot be enrolled.",
        )

    history = AuditTrail()

    objects = EnrolmentChecklistManager()

    def __unicode__(self):
        if self.eligible:
            return 'Eligible'
        else:
            return 'Not Eligible'

    def save(self, *args, **kwargs):
        self.registered_subject = self.household_member.registered_subject
        self.validate_or_clear()
        super(EnrolmentChecklist, self).save(*args, **kwargs)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError("household_member cannot be None for pk='\{0}\'".format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.household_member']

    def validate_or_clear(self):
        """Checks if eligible and if not clears PII fields."""
        self.eligible = True
        #self.reason_not_eligible = 'bad dog'
        #self.dob = None
        #self.gender = None
        #self.omang = uuid4()  # use a dummy value to maintain unique constraint
        #self.is_dob_estimated = None

    def get_report_datetime(self):
        return self.report_datetime

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household_member__household_structure__household__household_identifier')

    def composition(self):
        url = reverse('household_dashboard_url', kwargs={'dashboard_type': 'household', 'dashboard_model': 'household_structure', 'dashboard_id': self.household_member.household_structure.pk})
        return """<a href="{url}" />composition</a>""".format(url=url)
    composition.allow_tags = True

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Enrolment Checklist"
