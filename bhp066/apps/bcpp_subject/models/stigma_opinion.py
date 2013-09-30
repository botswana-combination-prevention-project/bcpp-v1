# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from edc.audit.audit_trail import AuditTrail
from apps.bcpp.choices import AGREE_STRONGLY
from .base_scheduled_visit_model import BaseScheduledVisitModel


class StigmaOpinion (BaseScheduledVisitModel):

    """CS002"""

    test_community_stigma = models.CharField(
        verbose_name=_("People are hesitant to take an HIV test due to"
                      " fear of people\'s reaction if the test result is positive for HIV."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    gossip_community_stigma = models.CharField(
        verbose_name=_("People talk badly about people living with or thought"
                      " to be living with HIV to others."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    respect_community_stigma = models.CharField(
        verbose_name=_("People living with or thought to be living with HIV"
                      " lose respect or standing."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_verbal_stigma = models.CharField(
        verbose_name=_("People living with or thought to be living with HIV"
                      " are verbally insulted, harassed and/or threatened."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_phyical_stigma = models.CharField(
        verbose_name=_("People living with or thought to be living with"
                      " HIV are sometimes physically assaulted."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_family_stigma = models.CharField(
        verbose_name=_("People living with or thought to be living with"
                      " HIV are now more accepted by others as there is now an effective"
                      " treatment available."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    fear_stigma = models.CharField(
        verbose_name=_("People living with HIV are less able to financially"
                      " support themselves and their families."),
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Stigma Opinion"
        verbose_name_plural = "Stigma Opinion"
