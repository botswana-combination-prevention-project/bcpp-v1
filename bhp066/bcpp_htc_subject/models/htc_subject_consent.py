from django.db import models
from django.utils.translation import ugettext as _
from edc.core.audit_trail.audit import AuditTrail
from edc.core.bhp_common.choices import YES_NO
from bcpp_household_member.models import BaseHouseholdMemberConsent
from .subject_off_study_mixin import SubjectOffStudyMixin


class HtcSubjectConsent(SubjectOffStudyMixin, BaseHouseholdMemberConsent):

    is_minor = models.CharField(
        verbose_name=_("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text='Subject is a minor if aged 16-17. A guardian must be present for consent. HIV status may NOT be revealed in the household.')

    history = AuditTrail()

    def get_subject_type(self):
        return 'htc_subject'

    class Meta:
        app_label = 'bcpp_htc_subject'
        unique_together = ('subject_identifier', 'survey')
