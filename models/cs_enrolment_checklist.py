from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.validators import eligible_if_yes, eligible_if_no
from bhp_common.choices import YES_NO, YES_NO_REFUSED
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bhp_registration.models import BaseRegisteredSubjectModel


class CsEnrolmentChecklist (BaseRegisteredSubjectModel):

    """CS008"""

    registration_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ])

    census_number = models.CharField(
        verbose_name="[Interviewer] Household number: ",
        max_length=5,
        help_text="if 'Not a census enumerated household,' STOP participant cannot be enrolled",
        )

    mental_capacity = models.CharField(
        verbose_name=("[Interviewer] Does the prospective participant have sufficient"
                      " mental capacity to provide considered informed consent? "),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
        )

    incarceration = models.CharField(
        verbose_name=("[Interviewer] Is the prospective participant currently under"
                      " involuntary incarceration? "),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_no, ],
        help_text=" if 'YES,' STOP participant cannot be enrolled",
        )

    citizen = models.CharField(
        verbose_name="[Interviewer] Is the prospective participant a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled",
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

    date_minor_signed = models.DateTimeField(
        verbose_name="[Interviewer] Date study ASSENT signed:",
        max_length=25,
        null=True,
        blank=True,
        help_text="For participants, aged 16 and 17 years only. If not signed, STOP participant cannot be enrolled.",
        )

    date_guardian_signed = models.DateTimeField(
        verbose_name="Date/Time study PARENT/GUARDIAN PERMISSION signed",
        max_length=25,
        null=True,
        blank=True,
        help_text=("For participants, aged 16 and 17 years only. If not signed, STOP participant cannot"
                   " be enrolled. END here for participants age 16 and 17 years"),
        )

    date_consent_signed = models.DateTimeField(
        verbose_name="Date/Time study CONSENT signed",
        max_length=25,
        help_text="If not signed, STOP participant cannot be enrolled.",
        )

    history = AuditTrail()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "CS Enrolment Checklist"
