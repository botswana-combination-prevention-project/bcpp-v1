from edc.audit.audit_trail import AuditTrail

from apps.bcpp_household_member.constants import UNDECIDED
from apps.bcpp_household_member.exceptions import MemberStatusError

from .base_member_status_model import BaseMemberStatusModel


class SubjectUndecided (BaseMemberStatusModel):

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.member_status != UNDECIDED:
            raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(UNDECIDED, self.household_member.member_status))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectUndecided, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
#         db_table = 'bcpp_subject_subjectundecided'
        verbose_name = "Subject Undecided"
        verbose_name_plural = "Subject Undecided"
        unique_together = ('registered_subject', 'survey',)
