from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import AGREE_STRONGLY, WHEREACCESS_CHOICE
from bhp066.apps.bcpp_list.models import MedicalCareAccess

from .base_scheduled_visit_model import BaseScheduledVisitModel


class AccessToCare (BaseScheduledVisitModel):

    access_care = models.CharField(
        verbose_name="In the past year, where do you MOST OFTEN get"
                     " medical care or treatment when you or someone in your family is sick or hurt?",
        max_length=50,
        choices=WHEREACCESS_CHOICE,
        null=True,
        help_text="supplemental")

    access_care_other = OtherCharField(
        null=True)

    medical_care_access = models.ManyToManyField(
        MedicalCareAccess,
        verbose_name="In the past year, where else have you obtained"
                     " medical care or treatment when you or someone in your family"
                     " is sick or hurt? (check all that apply)",
        null=True,
        help_text="supplemental")

    medical_care_access_other = OtherCharField(
        null=True)

    overall_access = models.CharField(
        verbose_name="If I need medical care, I can get seen by an"
                     " appropriate health professional without any trouble.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="supplemental")

    emergency_access = models.CharField(
        verbose_name="It is hard for me to get medical care in an emergency",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="supplemental")

    expensive_access = models.CharField(
        verbose_name="Sometimes I go without the medical care I need because"
                     " it is too expensive.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="supplemental")

    convenient_access = models.CharField(
        verbose_name="Places where I can get medical care are very conveniently located.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="supplemental")

    whenever_access = models.CharField(
        verbose_name="I am able to get medical care whenever I need it.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="supplemental")

    local_hiv_care = models.CharField(
        verbose_name="Would you be willing to come to the clinic within your "
                     "community to receive HIV care and treatment, if "
                     "available locally?",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="supplemental")

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Access to Care"
        verbose_name_plural = "Access to Care"
