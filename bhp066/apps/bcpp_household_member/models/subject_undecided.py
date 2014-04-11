from django.db import models

from edc.audit.audit_trail import AuditTrail

from .base_member_status_model import BaseMemberStatusModel

from apps.bcpp_household.exceptions import AlreadyReplaced


class SubjectUndecided (BaseMemberStatusModel):

    history = AuditTrail()

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectUndecided, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
#         db_table = 'bcpp_subject_subjectundecided'
        verbose_name = "Subject Undecided"
        verbose_name_plural = "Subject Undecided"
        unique_together = ('registered_subject', 'survey',)
