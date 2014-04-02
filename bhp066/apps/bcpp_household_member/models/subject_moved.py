from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.base.model.validators import date_not_future, date_not_before_study_start

from apps.bcpp_household.exceptions import AlreadyReplaced

from ..choices import MOVED_REASON, PLACE_SUBJECT_MOVED

from .base_member_status_model import BaseMemberStatusModel


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

    def save(self, *args, **kwargs):
        if self.household_structure.household.replaced_by:
            raise AlreadyReplaced('Model {0}-{1} has its container replaced.'.format(self._meta.object_name, self.pk))
        kwargs['reason'] = 'moved'
        kwargs['info_source'] = 'subject'
        self.survey = self.household_member.survey
        super(SubjectMoved, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
#         db_table = 'bcpp_subject_subjectmoved'
        verbose_name = "Subject Moved"
        verbose_name_plural = "Subject Moved"
        ordering = ['household_member']
