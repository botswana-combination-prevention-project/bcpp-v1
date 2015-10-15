from django.db import models

from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp.choices import AGREE_STRONGLY

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Stigma (BaseScheduledVisitModel):

    """CS002"""

    CONSENT_MODEL = SubjectConsent

    anticipate_stigma = models.CharField(
        verbose_name="Would you be, or have you ever been,"
                     " hesitant to take an HIV test due to fear of people\'s "
                     "reaction if you tested positive for HIV.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_shame_stigma = models.CharField(
        verbose_name="I would be ashamed if someone in my family had HIV.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="",
    )

    saliva_stigma = models.CharField(
        verbose_name="I fear that I could contract HIV if I come into contact"
                     " with the saliva of a person living with HIV.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="",
    )

    teacher_stigma = models.CharField(
        verbose_name="I think that if a teacher is living with HIV but"
                     " is not sick, he/she should be allowed to continue teaching in the school.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="",
    )

    children_stigma = models.CharField(
        verbose_name="Children living with HIV should be able to attend school"
                     " with children who are HIV negative.",
        max_length=25,
        choices=AGREE_STRONGLY,
        null=True,
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Stigma"
        verbose_name_plural = "Stigma"
