from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO

from apps.bcpp_household_member.constants import HTC, HTC_ELIGIBLE, REFUSED_HTC
from apps.bcpp_household_member.exceptions import MemberStatusError

from .base_member_status_model import BaseMemberStatusModel


class SubjectHtc(BaseMemberStatusModel):

    offered = models.CharField(
        verbose_name="Was the subject offered HTC",
        max_length=10,
        choices=YES_NO)

    outcome = models.CharField(
        verbose_name="The subject:",
        max_length=25,
        choices=(('accepted', 'Accepted HTC'), ('refused', 'Refused HTC'), ('N/A', 'Not applicable'), ),
        )

    comment = models.TextField(max_length=250, null=True, blank=True)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.member_status not in [HTC, HTC_ELIGIBLE, REFUSED_HTC]:
            raise MemberStatusError('Expected member status to be on of {0}. Got {1}'.format([HTC, HTC_ELIGIBLE, REFUSED_HTC], self.household_member.member_status))
        self.survey = self.household_member.survey
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        self.household_member.htc = True
        self.household_member.save()
        super(SubjectHtc, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Htc"
        verbose_name_plural = "Subject Htc"
        unique_together = ('registered_subject', 'survey',)
