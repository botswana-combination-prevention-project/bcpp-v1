from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField

from apps.bcpp.choices import YES_NO, YES_NO_UNSURE
from apps.bcpp_list.models import FamilyPlanning

from .base_scheduled_visit_model import BaseScheduledVisitModel


class ReproductiveHealth (BaseScheduledVisitModel):

    """A model completed by the user on the participant's reproductive health."""

    number_children = models.IntegerField(
        verbose_name=_("How many children have you given birth to? Please include any"
                       " children that may have died at (stillbirth) or after birth. "
                       "Do not include any current pregnancies or miscarriages that occur"
                       " early in pregnancy (prior to 20 weeks)."),
        max_length=2,
        default=0,
        help_text="",
        )

    menopause = models.CharField(
        verbose_name=_("Have you reached menopause (more than 12 months without a period)?"),
        max_length=3,
        choices=YES_NO,
        help_text="this also refers to pre-menopause",
        )

    family_planning = models.ManyToManyField(FamilyPlanning,
        verbose_name=_("In the past 12 months, have you used any methods to prevent"
                       " pregnancy ?"),
        null=True,
        blank=True,
        help_text="check all that apply",
        )
    family_planning_other = OtherCharField()

    currently_pregnant = models.CharField(
        verbose_name=_("Are you currently pregnant?"),
        null=True,
        blank=True,
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Reproductive Health"
        verbose_name_plural = "Reproductive Health"
