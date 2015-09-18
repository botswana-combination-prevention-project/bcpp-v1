from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from bhp066.apps.bcpp.choices import YES_NO
from .base_scheduled_model import BaseScheduledModel


class PositiveFollowup (BaseScheduledModel):

    """Positive Permissions to be contacted for follow-up"""

    contact_consent = models.CharField(
        verbose_name=_("My fellow counselors and I are available to help you"
                       " begin HIV care at the local health clinic.  Do you give"
                       " permission for counselors to contact you by telephone and"
                       " make home visits to make sure you get the care you need"),
        max_length=3,
        choices=YES_NO,
        help_text='',
        )

    contact_family = models.CharField(
        verbose_name=_("If we are unable to reach you, would you be willing to have me or"
                       " one of my fellow counselors contact a family member or friend who "
                       "would be able to reach you"),
        max_length=3,
        choices=YES_NO,
        help_text=''
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Positive Follow-up"
        verbose_name_plural = "Positive Follow-up"
