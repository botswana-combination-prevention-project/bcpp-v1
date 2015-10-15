from django.db import models

from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp.choices import AGREE_STRONGLY

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class StigmaOpinion (BaseScheduledVisitModel):

    """CS002"""
    CONSENT_MODEL = SubjectConsent

    test_community_stigma = models.CharField(
        verbose_name="People are hesitant to take an HIV test due to"
                     " fear of people\'s reaction if the test result is positive for HIV.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    gossip_community_stigma = models.CharField(
        verbose_name="People talk badly about people living with or thought"
                     " to be living with HIV to others.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    respect_community_stigma = models.CharField(
        verbose_name="People living with or thought to be living with HIV"
                     " lose respect or standing.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_verbal_stigma = models.CharField(
        verbose_name="People living with or thought to be living with HIV"
                     " are verbally insulted, harassed and/or threatened.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_phyical_stigma = models.CharField(
        verbose_name="People living with or thought to be living with"
                     " HIV are sometimes physically assaulted.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_family_stigma = models.CharField(
        verbose_name="People living with or thought to be living with"
                     " HIV are now more accepted by others as there is now an effective"
                     " treatment available.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    fear_stigma = models.CharField(
        verbose_name="People living with HIV are less able to financially"
                     " support themselves and their families.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Stigma Opinion"
        verbose_name_plural = "Stigma Opinion"
