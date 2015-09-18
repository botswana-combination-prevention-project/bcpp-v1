from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from bhp066.apps.bcpp.choices import YES_NO
from ..choices import TESTING_CENTRE, YES_NO_DECLINED
from .base_scheduled_model import BaseScheduledModel


class HtcHivTestingHistory (BaseScheduledModel):

    previous_testing = models.CharField(
        verbose_name=_("Have you ever previously been tested for HIV?"),
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    testing_place = models.CharField(
        verbose_name=_("Where did you last undergo HIV testing?"),
        max_length=50,
        choices=TESTING_CENTRE,
        null=True,
        blank=True,
        help_text="",
        )

    hiv_record = models.CharField(
        verbose_name=_("Is a record of your last HIV test available to review today?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DECLINED,
        )

    result_obtained = models.CharField(
        verbose_name=_("Was HIV- test result obtained in the past 3 months?"),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DECLINED,
        help_text="do not read aloud, use date recorded in card",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "HTC HIV Testing History"
        verbose_name_plural = "HTC HIV Testing History"
