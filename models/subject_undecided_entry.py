from django.db import models
from audit_trail.audit import AuditTrail
from bcpp_subject.models import SubjectUndecided
from bcpp_subject.choices import UNDECIDED_REASON
from bcpp_subject.managers import SubjectUndecidedEntryManager
from base_subject_entry import BaseSubjectEntry


class SubjectUndecidedEntry(BaseSubjectEntry):

    subject_undecided = models.ForeignKey(SubjectUndecided)

    subject_undecided_reason = models.CharField(
        verbose_name="Reason",
        max_length=100,
        choices=UNDECIDED_REASON,
     )

    history = AuditTrail()

    objects = SubjectUndecidedEntryManager()

    def natural_key(self):
        return (self.report_datetime,) + self.subject_undecided.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectundecided']

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = ('subject_undecided', 'report_datetime')
