from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bcpp.choices import AGREE_STRONGLY, WHEREACCESS_CHOICE
from bcpp_list.models import MedicalCareAccess
from base_scheduled_visit_model import BaseScheduledVisitModel


class AccessToCare (BaseScheduledVisitModel):

    """CS002"""

    access_care = models.CharField(
        verbose_name=("Supplemental AC1. In the past year, where do you MOST OFTEN get"
                      " medical care or treatment when you or someone in your family is sick or hurt?"),
        max_length=50,
        choices=WHEREACCESS_CHOICE,
        help_text="",
        )
    access_care_other = OtherCharField()

    medical_care_access = models.ManyToManyField(MedicalCareAccess,
        verbose_name=("Supplemental AC2. In the past year, where else have you obtained"
                      " medical care or treatment when you or someone in your family"
                      " is sick or hurt?"),
        help_text="(check all that apply)",
        )
    medical_care_access_other = OtherCharField()

    overall_access = models.CharField(
        verbose_name=("Supplemental AC3. If I need medical care, I can get seen by an"
                        " appropriate health professional without any trouble."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    emergency_access = models.CharField(
        verbose_name="Supplemental AC4. It is hard for me to get medical care in an emergency",
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    expensive_access = models.CharField(
        verbose_name="Supplemental AC5. Sometimes I go without the medical care I need because it is too expensive.",
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    convenient_access = models.CharField(
        verbose_name="Supplemental AC6. Places where I can get medical care are very conveniently located.",
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    whenever_access = models.CharField(
        verbose_name="Supplemental AC7. I am able to get medical care whenever I need it.",
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Access to Care"
        verbose_name_plural = "Access to Care"
