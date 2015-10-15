from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import MARITALSTATUS_CHOICE
from bhp066.apps.bcpp_list.models import LiveWith, Religion, EthnicGroups

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Demographics (BaseScheduledVisitModel):

    """A model completed by the user of the basic demographics of the participant."""

    CONSENT_MODEL = SubjectConsent

    religion = models.ManyToManyField(
        Religion,
        verbose_name="What is your religion affiliation?",
        help_text="")

    religion_other = OtherCharField()

    ethnic = models.ManyToManyField(
        EthnicGroups,
        verbose_name="What is your ethnic group?",
        help_text="Ask for the original ethnic group")

    ethnic_other = OtherCharField()

    marital_status = models.CharField(
        verbose_name="What is your current marital status?",
        max_length=55,
        choices=MARITALSTATUS_CHOICE,
        help_text="")

    num_wives = models.IntegerField(
        verbose_name="WOMEN: How many wives does your husband have (including traditional marriage),"
                     " including yourself?",
        max_length=2,
        null=True,
        blank=True,
        help_text="Leave blank if participant does not want to respond. (women only)")

    husband_wives = models.IntegerField(
        verbose_name="MEN: How many wives do you have, including traditional marriage?",
        max_length=2,
        null=True,
        blank=True,
        help_text="Leave blank if participant does not want to respond. (men only)")

    live_with = models.ManyToManyField(
        LiveWith,
        verbose_name="Who do you currently live with ?",
        help_text="[indicate all that apply]")

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Demographics"
        verbose_name_plural = "Demographics"
