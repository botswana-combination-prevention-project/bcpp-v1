from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import AGREE_STRONGLY
from bcpp_list.models import MedicalCareAccess
from base_scheduled_visit_model import BaseScheduledVisitModel


class AccessToCare (BaseScheduledVisitModel):
    
    """CS002"""
    
    often_medicalcare = models.CharField(
        verbose_name=("Supplemental AC1. In the past year, where do you MOST OFTEN get"
                      " medical care or treatment when you or someone in your family is sick or hurt?"),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    whereaccess = models.ManyToManyField(MedicalCareAccess,
        verbose_name=("Supplemental AC2. In the past year, where else have you obtained"
                      " medical care or treatment when you or someone in your family"
                      " is sick or hurt?"),
        help_text="(check all that apply)",
        )

    overallaccess = models.CharField(
        verbose_name=("Supplemental AC3. If I need medical care, I can get seen by an"
                        " appropriate health professional without any trouble."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    emergencyaccess = models.CharField(
        verbose_name = "Supplemental AC4. It is hard for me to get medical care in an emergency",
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    expensiveaccess = models.CharField(
        verbose_name = "Supplemental AC5. Sometimes I go without the medical care I need because it is too expensive.",
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    convenientaccess = models.CharField(
        verbose_name = "Supplemental AC6. Places where I can get medical care are very conveniently located.",
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    wheneverlaccess = models.CharField(
        verbose_name = "Supplemental AC7. I am able to get medical care whenever I need it.",
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_accesstocare_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Access to Care"
        verbose_name_plural = "Access to Care"
