from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_base_model.validators import datetime_is_future
from bhp_crypto.fields import EncryptedCharField
from bhp_base_model.fields import OtherCharField
from bcpp_list.models import SubjectAbsenteeReason
from bcpp_subject.choices import NEXT_APPOINTMENT_SOURCE, ABSENTEE_STATUS
from base_member_status_model import BaseMemberStatusModel
# from base_subject_visit_model import BaseSubjectVisitModel
from base_scheduled_visit_model import BaseScheduledVisitModel


class SubjectAbsentee(BaseMemberStatusModel):

    subject_absentee_status = models.CharField(
        verbose_name="Absentee status",
        max_length=25,
        choices=ABSENTEE_STATUS,
        help_text=("Change the absentee status from 'absent' to 'no longer absent'"
                   " if and when the subject is seen"),
        default='absent',
        editable=False
        )

    history = AuditTrail()

    def get_absolute_url(self):
        if self.id:
            return reverse('admin:bcpp_subject_subjectabsentee_change', args=(self.id,))
        else:
            return reverse('admin:bcpp_subject_subjectabsentee_add')

    def member_status_string(self):
        return 'ABSENT'

    def save(self, *args, **kwargs):
        self.survey = self.household_structure_member.survey
        super(SubjectAbsentee, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Absentee"
        verbose_name_plural = "Subject Absentee"
        unique_together = ('registered_subject', 'survey',)


class SubjectAbsenteeReport(BaseScheduledVisitModel):

    subject_absentee_reason = models.ForeignKey(SubjectAbsenteeReason,
        verbose_name="Reason for absence?"
        )

    subject_absentee_reason_other = OtherCharField()

    subject_absentee_status = models.CharField(
        verbose_name="Absentee status",
        max_length=25,
        choices=ABSENTEE_STATUS,
        help_text=("Change the absentee status from 'absent' to 'no longer absent' "
                   "if and when the subject is seen"),
        default='absent',
        editable=False
        )

    next_appt_datetime = models.DateTimeField(
        verbose_name="Follow-up appointment date and time",
        validators=[datetime_is_future, ],
        help_text="The date and time to meet with the subject"
        )

    """ add list of 'times' as morning, afternoon, evening """

    next_appt_datetime_source = models.CharField(
        verbose_name="With whom did you discuss the appointment date and time?",
        max_length=25,
        choices=NEXT_APPOINTMENT_SOURCE,
        help_text=''
        )

    contact_details = EncryptedCharField(
        null=True,
        blank=True,
        editable=False,
        help_text=('Information that can be used to contact someone, '
                   'preferrably the subject, to confirm the appointment'),
        )

    comment = models.TextField(
        verbose_name="Comments",
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: DO NOT include any names or other personally identifying '
           'information in this comment')
        )

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.subject_visit)

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectabsenteereport_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Absentee Report"
        verbose_name_plural = "Subject Absentee Report"
