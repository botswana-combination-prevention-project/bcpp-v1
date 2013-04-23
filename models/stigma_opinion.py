# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bcpp.choices import AGREE_STRONGLY
from base_scheduled_visit_model import BaseScheduledVisitModel


class StigmaOpinion (BaseScheduledVisitModel):
    
    """CS002"""
    
    testcommunitystigma = models.CharField(
        verbose_name=("Supplemental ST6. People are hesitant to take an HIV test due to"
                      " fear of people’s reaction if the test result is positive for HIV."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    gossipcommunitystigma = models.CharField(
        verbose_name=("Supplemental ST7. People talk badly about people living with or thought"
                      " to be living with HIV to others."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    respectcommunitystigma = models.CharField(
        verbose_name=("Supplemental ST8. People living with or thought to be living with HIV"
                      " lose respect or standing."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    enactedverbalstigma = models.CharField(
        verbose_name=("Supplemental ST9. People living with or thought to be living with HIV"
                      " are verbally insulted, harassed and/or threatened."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    enactedphyicalstigma = models.CharField(
        verbose_name=("Supplemental ST10. People living with or thought to be living with"
                      " HIV are sometimes physically assaulted."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    enactedfamilystigma = models.CharField(
        verbose_name=("Supplemental ST11. People living with or thought to be living with"
                      " HIV are now more accepted by others as there is now an effective"
                      " treatment available."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    fearstigma = models.CharField(
        verbose_name=("Supplemental ST12. People living with HIV are less able to financially"
                      " support themselves and their families."),
        max_length = 15,
        choices = AGREE_STRONGLY,
        help_text="",
        )

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_stigmaopinion_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Stigma Opinion"
        verbose_name_plural = "Stigma Opinion"
