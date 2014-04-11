from edc.audit.audit_trail import AuditTrail

from .base_member_status_model import BaseMemberStatusModel

from apps.bcpp_household.exceptions import AlreadyReplaced


class SubjectUndecided (BaseMemberStatusModel):

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.household_structure.household.replaced_by:
            raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectUndecided, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
#         db_table = 'bcpp_subject_subjectundecided'
        verbose_name = "Subject Undecided"
        verbose_name_plural = "Subject Undecided"
        unique_together = ('registered_subject', 'survey',)
