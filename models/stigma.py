# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from audit_trail.audit import AuditTrail
from bcpp.choices import AGREE_STRONGLY
from base_scheduled_visit_model import BaseScheduledVisitModel


class Stigma (BaseScheduledVisitModel):

    """CS002"""

    anticipate_stigma = models.CharField(
        verbose_name=_("Would you be, or have you ever been,"
                      " hesitant to take an HIV test due to fear of people\'s "
                      "reaction if you tested positive for HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    enacted_shame_stigma = models.CharField(
        verbose_name=_("I would be ashamed if someone in my family had HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    saliva_stigma = models.CharField(
        verbose_name=_("I fear that I could contract HIV if I come into contact"
                      " with the saliva of a person living with HIV."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    teacher_stigma = models.CharField(
        verbose_name=_("I think that if a female teacher is living with HIV but"
                      " is not sick, she should be allowed to continue teaching in the school."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    children_stigma = models.CharField(
        verbose_name=_("Children living with HIV should be able to attend school"
                      " with children who are HIV negative."),
        max_length=25,
        choices=AGREE_STRONGLY,
        help_text="supplemental",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Stigma"
        verbose_name_plural = "Stigma"
