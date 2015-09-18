from django.db import models
from django.utils.translation import ugettext as _
from bhp066.apps.bcpp.choices import YES_NO
from ..choices import PARTNER_HIV_STATUS
from .base_scheduled_model import BaseScheduledModel


class BasePartner (BaseScheduledModel):

    partner_tested = models.CharField(
        verbose_name=_("Has this partner ever been tested for HIV?"),
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    parter_status = models.CharField(
        verbose_name=_("What is this partner\'s HIV status?"),
        max_length=25,
        choices=PARTNER_HIV_STATUS,
        )

    partner_residency = models.CharField(
        verbose_name=_("Does this partner live in this community?"),
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    class Meta:
        abstract = True
