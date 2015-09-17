from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


class SubjectUndecided (BaseMemberStatusModel):
    """A system model that links "undecided" information to a household member."""
    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_member.household_structure.household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(
                self.subject_undecided.household_member.household_structure.household.household_identifier))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        try:
            update_fields = kwargs.get('update_fields') + ['registered_subject', 'survey']
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(SubjectUndecided, self).save(*args, **kwargs)

    def deserialize_prep(self, **kwargs):
        # SubjectUndecided being deleted by an IncommingTransaction, we go ahead and delete it.
        # This happens when we switch status from absentee and there are no absentee entries
        # attached to this SubjectUndecided.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Undecided"
        verbose_name_plural = "Subject Undecided"
        unique_together = ('registered_subject', 'survey',)
