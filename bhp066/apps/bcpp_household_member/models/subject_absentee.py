from django.db import models

from edc.audit.audit_trail import AuditTrail

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

    def member_status_string(self):
        return 'ABSENT'

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(SubjectAbsentee, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
#         db_table = 'bcpp_subject_subjectabsentee'
        verbose_name = "Subject Absentee"
        verbose_name_plural = "Subject Absentee"
        unique_together = ('registered_subject', 'survey',)
