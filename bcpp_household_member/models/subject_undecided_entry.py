from django.db import models

from simple_history.models import HistoricalRecords

from ..choices import UNDECIDED_REASON
from ..managers import SubjectUndecidedEntryManager

from .base_subject_entry import BaseSubjectEntry
from .subject_undecided import SubjectUndecided


class SubjectUndecidedEntry(BaseSubjectEntry):
    """A model completed by the user that captures information on the undecided status
    of a household member potentially eligible for BHS."""
    subject_undecided = models.ForeignKey(SubjectUndecided)

    subject_undecided_reason = models.CharField(
        verbose_name="Reason",
        max_length=100,
        choices=UNDECIDED_REASON)

    history = HistoricalRecords()

    objects = SubjectUndecidedEntryManager()

    @property
    def inline_parent(self):
        return self.subject_undecided

    def natural_key(self):
        return (self.report_datetime,) + self.subject_undecided.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectundecided']

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Undecided Entry"
        verbose_name_plural = "Subject Undecided Entries"
        unique_together = ('subject_undecided', 'report_datetime')
