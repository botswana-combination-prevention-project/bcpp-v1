from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from edc.choices.common import YES_NO, POS_NEG, YES_NO_DONT_KNOW
from ..choices import SYMPTOMS
from .base_scheduled_model import BaseScheduledModel


class HtcHivResult(BaseScheduledModel):

    todays_result = models.CharField(
        verbose_name=_("Today\'s results:"),
        max_length=15,
        choices=POS_NEG,
        help_text='',
    )

    couples_testing = models.CharField(
        verbose_name=_("Did testing and counseling occur through couples testing today?"),
        max_length=15,
        choices=YES_NO,
        help_text='',
    )
    # We need clarification here as to the type of id used here. Is it Omang?
    partner_id = models.CharField(
        verbose_name=_("What is the unique identification number for the other member of the couple?"),
        max_length=25,
        null=True,
        blank=True,
        help_text='',
    )

    symptoms = models.CharField(
        verbose_name=_("Does the client currently have any of the following symptoms?"),
        max_length=75,
        choices=SYMPTOMS,
        help_text='',
    )

    family_tb = models.CharField(
        verbose_name=_("Have any of the client\'s family members been diagnosed with tuberculosis?"),
        max_length=15,
        choices=YES_NO_DONT_KNOW,
        help_text='',
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "HIV test result"
        verbose_name_plural = "HIV test result"
