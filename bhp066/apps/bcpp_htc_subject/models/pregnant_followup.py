from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from bhp066.apps.bcpp.choices import YES_NO
from .base_scheduled_model import BaseScheduledModel


class PregnantFollowup (BaseScheduledModel):

    """Permission to contact for follow up for pregnant women"""

    contact_consent = models.CharField(
        verbose_name=_("It is recommended that pregnant women receive antenatal care for their health"
                       " and their baby\'s health.  This care includes an HIV test during the third"
                       " trimester of pregnancy.  Counselors are available to help you receive HIV"
                       " testing during pregnancy.  Do you give permission for counselors to contact"
                       " you by telephone and home visits?"),
        max_length=3,
        choices=YES_NO,
        help_text='',
        )

    contact_family = models.CharField(
        verbose_name=_("If we are unable to reach you, would you be willing to have me or one of my"
                       " fellow counselors contact a family member or friend who would be able to reach you?"),
        max_length=3,
        choices=YES_NO,
        help_text='',
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Pregnant Follow-up"
        verbose_name_plural = "Pregnant Follow-up"
