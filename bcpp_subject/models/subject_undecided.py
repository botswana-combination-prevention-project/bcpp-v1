from edc_core.audit_trail.audit import AuditTrail
from bcpp_household_member.models import BaseMemberStatusModel


class SubjectUndecided (BaseMemberStatusModel):

    history = AuditTrail()

    def member_status_string(self):
        return 'UNDECIDED'

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(SubjectUndecided, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Undecided"
        verbose_name_plural = "Subject Undecided"
        unique_together = ('registered_subject', 'survey',)
