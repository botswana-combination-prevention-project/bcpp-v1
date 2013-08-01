from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO
from bcpp.choices import EDUCATION_CHOICE
from bcpp_subject.choices import MONTHLY_INCOME, JOB_TYPE, REASON_UNEMPLOYED, JOB_DESCRIPTION
from base_scheduled_visit_model import BaseScheduledVisitModel


class Education (BaseScheduledVisitModel):

    """CS002"""

    education = models.CharField(
        verbose_name=_("What is your highest level of education attainment?"),
        max_length=65,
        choices=EDUCATION_CHOICE,
        help_text="",
        )

    working = models.CharField(
        verbose_name=_("Are you currently working?"),
        choices=YES_NO,
        max_length=3,
        help_text="",
        )

    job_type = models.CharField(
        verbose_name=_("In your main job what type of work do you do?"),
        max_length=45,
        choices=JOB_TYPE,
        help_text="",
        )

    reason_unemployed = models.CharField(
        verbose_name=_("What is the reason why you are not working?"),
        max_length=65,
        blank=True,
        null=True,
        choices=REASON_UNEMPLOYED,
        help_text="",
        )

    job_description = models.CharField(
        verbose_name=_("Describe the work that you do or did in your most recent"
                      " job. If you have more than one profession, choose the"
                      " one you spend the most time doing."),
        max_length=65,
        choices=JOB_DESCRIPTION,
        help_text="",
        )

    monthly_income = models.CharField(
        verbose_name=_("In the past month, how much money did you earn from"
                      " work you did or received in payment [retirement benefits"
                      " child maintenance, food basket, etc]?"),
        max_length=25,
        choices=MONTHLY_INCOME,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Education"
        verbose_name_plural = "Education"
