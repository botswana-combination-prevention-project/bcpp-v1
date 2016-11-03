from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from bhp066.apps.bcpp_list.models import ReferredFor, ReferredTo
from .base_scheduled_model import BaseScheduledModel


class Referral(BaseScheduledModel):

    referred_for = models.ManyToManyField(
        ReferredFor,
        verbose_name=_("Client referred FOR:"),
        help_text='(tick all that apply)'
    )

    referred_to = models.ManyToManyField(
        ReferredTo,
        verbose_name=_("Client referred TO:"),
        help_text='(tick all that apply)',
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Referral"
        verbose_name_plural = "referral"
