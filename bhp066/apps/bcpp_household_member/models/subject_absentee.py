from django.db import models

from edc.audit.audit_trail import AuditTrail

from apps.bcpp_household_member.constants import ABSENT
from apps.bcpp_household_member.exceptions import MemberStatusError

from ..choices import ABSENTEE_STATUS

from .base_member_status_model import BaseMemberStatusModel


class SubjectAbsentee(BaseMemberStatusModel):

    subject_absentee_status = models.CharField(
        verbose_name="Absentee status",
        max_length=25,
        choices=ABSENTEE_STATUS,
        help_text=("Change the absentee status from 'absent' to 'no longer absent'"
                   " if and when the subject is seen"),
        default='absent',
        editable=False
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.member_status != ABSENT:
            raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(ABSENT, self.household_member.member_status))
        self.survey = self.household_member.survey
        super(SubjectAbsentee, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
#         db_table = 'bcpp_subject_subjectabsentee'
        verbose_name = "Subject Absentee"
        verbose_name_plural = "Subject Absentee"
        unique_together = ('registered_subject', 'survey',)
