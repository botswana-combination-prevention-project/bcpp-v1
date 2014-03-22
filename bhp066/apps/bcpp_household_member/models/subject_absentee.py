from edc.audit.audit_trail import AuditTrail

from apps.bcpp_household_member.constants import ABSENT
from apps.bcpp_household_member.exceptions import MemberStatusError

from .base_member_status_model import BaseMemberStatusModel


class SubjectAbsentee(BaseMemberStatusModel):

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.member_status != ABSENT:
            raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(ABSENT, self.household_member.member_status))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectAbsentee, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Absentee"
        verbose_name_plural = "Subject Absentee"
        unique_together = ('registered_subject', 'survey',)
