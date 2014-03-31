from edc.audit.audit_trail import AuditTrail

from .base_member_status_model import BaseMemberStatusModel


class SubjectAbsentee(BaseMemberStatusModel):

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectAbsentee, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Absentee"
        verbose_name_plural = "Subject Absentee"
        unique_together = ('registered_subject', 'survey',)
