from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from edc.choices.common import POS_NEG_ONLY
from ..choices import YES_NO_DECLINED
from .base_scheduled_model import BaseScheduledModel


class LastHivRecord (BaseScheduledModel):

    recorded_test = models.DateField(
        verbose_name=_("Recorded date of previous test:"),
        help_text="",
    )

    recorded_result = models.CharField(
        verbose_name=_("Recorded result of previous test:"),
        max_length=15,
        choices=POS_NEG_ONLY,
        help_text="",
    )

    attended_hiv_care = models.CharField(
        verbose_name=_("Have you ever attended a health clinic for HIV care?"),
        max_length=15,
        choices=YES_NO_DECLINED,
    )

    hiv_care_clinic = models.CharField(
        verbose_name=_("What is the name of the clinic most recently visited for HIV care?"),
        max_length=25,
        null=True,
        blank=True,
    )

    hiv_care_card = models.CharField(
        verbose_name=_("Do you have an ART card or HIV care enrollment card available to review today?"),
        max_length=25,
        choices=YES_NO_DECLINED,
        help_text="Check yes if client shows card to counselor, check no if client does not show card.",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Last HIV Record"
        verbose_name_plural = "Last HIV Record"
