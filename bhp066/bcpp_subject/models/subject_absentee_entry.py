from django.db import models
from edc.core.audit_trail.audit import AuditTrail
from ..models import SubjectAbsentee
from ..choices import ABSENTEE_REASON
from ..managers import SubjectAbsenteeEntryManager
from .base_subject_entry import BaseSubjectEntry


class SubjectAbsenteeEntry(BaseSubjectEntry):

    subject_absentee = models.ForeignKey(SubjectAbsentee)

    reason = models.CharField(
        verbose_name="Reason?",
        max_length=100,
        choices=ABSENTEE_REASON,
        )

    history = AuditTrail()

    objects = SubjectAbsenteeEntryManager()

    def inline_parent(self):
        return self.subject_absentee

    def natural_key(self):
        return (self.report_datetime, ) + self.subject_absentee.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectabsentee', ]

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Absentee Entry"
        verbose_name_plural = "Subject Absentee Entry"
        unique_together = ('subject_absentee', 'report_datetime')
