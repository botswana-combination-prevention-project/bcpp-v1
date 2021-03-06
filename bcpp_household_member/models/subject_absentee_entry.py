from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from ..choices import ABSENTEE_REASON
from ..managers import SubjectAbsenteeEntryManager

from .subject_absentee import SubjectAbsentee
from .model_mixins import SubjectEntryMixin


class SubjectAbsenteeEntry(SubjectEntryMixin, BaseUuidModel):
    """A model completed by the user that indicates the reason a household member
    is absent for each time the RA visits."""

    subject_absentee = models.ForeignKey(SubjectAbsentee)

    reason = models.CharField(
        verbose_name="Reason?",
        max_length=100,
        choices=ABSENTEE_REASON)

    history = HistoricalRecords()

    objects = SubjectAbsenteeEntryManager()

    def __str__(self):
        return '{} {}'.format(self.report_datetime.strftime('%Y-%m-%d'), self.reason[0:20])

    @property
    def inline_parent(self):
        return self.subject_absentee

    @property
    def absent(self):
        return self.subject_absentee.household_member.absent

    def natural_key(self):
        return (self.report_datetime, ) + self.subject_absentee.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectabsentee', ]

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Absentee Entry"
        verbose_name_plural = "Subject Absentee Entries"
        unique_together = ('subject_absentee', 'report_datetime')
