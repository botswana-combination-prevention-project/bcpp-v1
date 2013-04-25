from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.fields import OtherCharField
from bcpp_list.models import SubjectAbsenteeReason
from bcpp_subject.models import SubjectAbsentee
from bcpp_subject.choices import ABSENTEE_REASON
from base_subject_entry import BaseSubjectEntry
from bcpp_subject.managers import SubjectAbsenteeEntryManager


class SubjectAbsenteeEntry(BaseSubjectEntry):

    subject_absentee = models.ForeignKey(SubjectAbsentee)

    reason = models.CharField(
        verbose_name="Reason?",
        max_length=100,
        choices=ABSENTEE_REASON,
        )

    # TODO: remove after conversion
    subject_absentee_reason = models.ForeignKey(SubjectAbsenteeReason,
        verbose_name="Reason for absence?",
        null=True,
        editable=False,
        )

    # TODO: remove after conversion
    subject_absentee_reason_other = OtherCharField(null=True, editable=False)

    history = AuditTrail()

    objects = SubjectAbsenteeEntryManager()

    def natural_key(self):
        return (self.report_datetime, ) + self.subject_absentee.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectabsentee', 'bcpp_subject.subjectabsenteereason']

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Absentee Entry"
        verbose_name_plural = "Subject Absentee Entry"
        unique_together = ('subject_absentee', 'report_datetime')
