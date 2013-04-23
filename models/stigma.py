# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import AGREE_STRONGLY
from base_scheduled_visit_model import BaseScheduledVisitModel


class Stigma (BaseScheduledVisitModel):
    
    """CS002"""
    
    anticipatestigma = models.CharField(
        verbose_name=("Supplemental ST1. Would you be, or have you ever been,"
                      " hesitant to take an HIV test due to fear of people’s "
                      "reaction if you tested positive for HIV."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    enactedshamestigma = models.CharField(
        verbose_name = "Supplemental ST2. I would be ashamed if someone in my family had HIV.",
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    salivastigma = models.CharField(
        verbose_name=("Supplemental ST3. I fear that I could contract HIV if I come into contact"
                      " with the saliva of a person living with HIV."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    teacherstigma = models.CharField(
        verbose_name=("Supplemental ST4. I think that if a female teacher is living with HIV but"
                      " is not sick, she should be allowed to continue teaching in the school."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    childrenstigma = models.CharField(
        verbose_name=("Supplemental ST5. Children living with HIV should be able to attend school"
                      " with children who are HIV negative."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_stigma_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Stigma"
        verbose_name_plural = "Stigma"
