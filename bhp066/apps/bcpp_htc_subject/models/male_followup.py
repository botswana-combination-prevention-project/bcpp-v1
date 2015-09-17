from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from apps.bcpp.choices import YES_NO
from .base_scheduled_model import BaseScheduledModel


class MaleFollowup (BaseScheduledModel):

    """Male Permissions to be contacted for follow-up"""

    contact_consent = models.CharField(
        verbose_name=_("My fellow counselors and I are available to help you decide if circumcision"
                       " is right for you   and to access male circumcision services.  If we try to"
                       " call you and miss you, the caller will not leave any detailed message but"
                       " only his name and number. If someone asks, we will just say we are doing"
                       " mobilization for men\'s health.  Do you give permission for counselors"
                       " to contact you by telephone and home visits?"),
        max_length=3,
        choices=YES_NO,
        help_text='',
        )

    contact_family = models.CharField(
        verbose_name=_("If we are unable to reach you, would you be willing to have me or one"
                       " of my fellow counselors contact a family member or friend who would be"
                       " able to reach you?  The caller will not leave any detailed message but"
                       " only his name and number."),
        max_length=3,
        choices=YES_NO,
        help_text='',
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_htc_subject'
        verbose_name = "Male Follow-up"
        verbose_name_plural = "Male Follow-up"
