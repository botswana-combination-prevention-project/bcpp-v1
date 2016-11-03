from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from ..choices import EDUCATION, EMPLOYMENT, MARITAL_STATUS, ALCOHOL_INTAKE
from .base_scheduled_model import BaseScheduledModel


class DemographicsRisk (BaseScheduledModel):

    education = models.CharField(
        verbose_name=_("What is your highest level of education have you completed?"),
        max_length=75,
        choices=EDUCATION,
        help_text="",
    )

    employment = models.CharField(
        verbose_name=_("What is your current employment status?"),
        max_length=45,
        choices=EMPLOYMENT,
        help_text="",
    )

    marital_status = models.IntegerField(
        verbose_name=_("What is your current marital status?"),
        max_length=35,
        choices=MARITAL_STATUS,
        help_text="",
    )

    alcohol_intake = models.CharField(
        verbose_name=_("Now I would like to ask you about how frequently you drink alcohol."
                       "  In the past THREE months, how often  have you had a "
                       "drink containing alcohol?"),
        max_length=25,
        choices=ALCOHOL_INTAKE,
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Demographics & Risk Factors"
        verbose_name_plural = "Demographics & Risk Factors"
