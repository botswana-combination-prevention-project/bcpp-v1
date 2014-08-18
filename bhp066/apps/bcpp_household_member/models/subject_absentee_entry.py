from django.db import models

from edc.audit.audit_trail import AuditTrail

from apps.bcpp_household.exceptions import AlreadyReplaced
from apps.bcpp_household_member.classes import HouseholdMemberHelper

from ..choices import ABSENTEE_REASON
from ..managers import SubjectAbsenteeEntryManager

from .base_subject_entry import BaseSubjectEntry
from .subject_absentee import SubjectAbsentee


class SubjectAbsenteeEntry(BaseSubjectEntry):

    subject_absentee = models.ForeignKey(SubjectAbsentee)

    reason = models.CharField(
        verbose_name="Reason?",
        max_length=100,
        choices=ABSENTEE_REASON)

    history = AuditTrail()

    objects = SubjectAbsenteeEntryManager()

    def save(self, *args, **kwargs):
        if self.subject_absentee.household_member.household_structure.household.replaced_by:
            raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
        household_member_helper = HouseholdMemberHelper(self.subject_absentee.household_member)
        if not self.id:
            household_member = self.subject_absentee.household_member
            household_member.visit_attempts += 1
            household_member.absent = False
            if household_member.visit_attempts >= 3:
                household_member.absent = True
            household_member.member_status = household_member_helper.calculate_member_status_without_hint()
            household_member.save()
        super(SubjectAbsenteeEntry, self).save(*args, **kwargs)

    @property
    def inline_parent(self):
        return self.subject_absentee

    def natural_key(self):
        return (self.report_datetime, ) + self.subject_absentee.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectabsentee', ]

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Absentee Entry"
        verbose_name_plural = "Subject Absentee Entries"
        unique_together = ('subject_absentee', 'report_datetime')
