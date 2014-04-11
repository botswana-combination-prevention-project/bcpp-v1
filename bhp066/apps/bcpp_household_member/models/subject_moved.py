from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.base.model.validators import date_not_future, date_not_before_study_start

from apps.bcpp_household.exceptions import AlreadyReplaced

from ..choices import MOVED_REASON, PLACE_SUBJECT_MOVED

from .base_member_status_model import BaseMemberStatusModel


class SubjectMoved(BaseMemberStatusModel):

    moved_date = models.DateField(
        verbose_name=_("Date subject moved?"),
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")
    moved_reason = models.CharField(
        verbose_name=_("Reason subject moved?"),
        choices=MOVED_REASON,
        max_length=15,
        help_text="Indicate the reason the individual moved")
    moved_reason_other = models.TextField(
        verbose_name="If Other please specify..",
        max_length=250,
        blank=True)
    place_moved = models.CharField(
        verbose_name=_("Where has the subject moved?"),
        choices=PLACE_SUBJECT_MOVED,
        max_length=25,
        help_text="")
    area_moved = models.CharField(
        verbose_name=_("Specific area where subject has moved?"),
        max_length=35,
        help_text="")
    contact_details = EncryptedTextField(
        null=True,
        blank=True,
        help_text=('Information to contact the subject, to confirm the next appointment if any'))
    comment = models.CharField(
        verbose_name=_("Comment"),
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
           'information in this comment'))

    history = AuditTrail()

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
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
