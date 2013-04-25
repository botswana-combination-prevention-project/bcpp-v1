from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_crypto.fields import EncryptedTextField
from bhp_base_model.validators import date_not_future, date_not_before_study_start
from bcpp_subject.choices import MOVED_REASON, PLACE_SUBJECT_MOVED
from base_member_status_model import BaseMemberStatusModel


class SubjectMoved(BaseMemberStatusModel):

    moved_date = models.DateField(
        verbose_name="Date subject moved?",
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")
    moved_reason = models.CharField(
        verbose_name="Reason subject moved?",
        choices=MOVED_REASON,
        max_length=15,
        help_text="Indicate the reason the individual moved")
    moved_reason_other = models.TextField(
        verbose_name="If Other please specify..",
        max_length=250,
        blank=True)
    place_moved = models.CharField(
        verbose_name="Where has the subject moved?",
        choices=PLACE_SUBJECT_MOVED,
        max_length=25,
        help_text="")
    area_moved = models.CharField(
        verbose_name="Specific area where subject has moved?",
        max_length=35,
        help_text="")
    contact_details = EncryptedTextField(
        null=True,
        blank=True,
        help_text=('Information to contact the subject, to confirm the next appointment if any'))
    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
           'information in this comment'))

    history = AuditTrail()

    def member_status_string(self):
        return 'MOVED'

    def post_save_update_hsm_status(self):
        self.household_structure_member.lives_in_household = 'No'
        super(SubjectMoved, self).post_save_update_hsm_status()

    def save(self, *args, **kwargs):
        kwargs['reason'] = 'moved'
        kwargs['info_source'] = 'subject'
        self.survey = self.household_structure_member.survey
        super(SubjectMoved, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.id:
            return reverse('admin:bcpp_subject_subjectmoved_change', args=(self.id,))
        else:
            return reverse('admin:bcpp_subject_subjectmoved_add')

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Moved"
        verbose_name_plural = "Subject Moved"
        ordering = ['household_structure_member']
