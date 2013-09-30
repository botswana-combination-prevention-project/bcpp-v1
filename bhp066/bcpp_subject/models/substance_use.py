from django.db import models
from django.utils.translation import ugettext as _
from edc.audit.audit_trail import AuditTrail
from bcpp.choices import ALCOHOL_CHOICE, YES_NO_DONT_ANSWER
from .base_scheduled_visit_model import BaseScheduledVisitModel


class SubstanceUse (BaseScheduledVisitModel):

    alcohol = models.CharField(
        verbose_name=_("In the past month, how often did you consume alcohol?"),
        max_length=25,
        choices=ALCOHOL_CHOICE,
        help_text="If participant does not know exactly, ask to give a best guess.",
        )

    smoke = models.CharField(
        verbose_name=_("Do you currently smoke any tobacco products, such as"
                      " cigarettes, cigars, or pipes?"),
        max_length=25,
        choices=YES_NO_DONT_ANSWER,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Substance Use"
        verbose_name_plural = "Substance Use"
