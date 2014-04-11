from django.db import models

from edc.audit.audit_trail import AuditTrail

from apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


class SubjectAbsentee(BaseMemberStatusModel):

    history = AuditTrail()

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectAbsentee, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Absentee"
        verbose_name_plural = "Subject Absentee"
        unique_together = ('registered_subject', 'survey',)
