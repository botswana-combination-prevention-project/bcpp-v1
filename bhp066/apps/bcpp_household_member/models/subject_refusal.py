from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import date_not_future, date_not_before_study_start

from apps.bcpp.choices import WHYNOPARTICIPATE_CHOICE

from .base_member_status_model import BaseMemberStatusModel


class SubjectRefusal (BaseMemberStatusModel):

    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")

    why_no_participate = models.CharField(
        verbose_name=("We respect your decision to decline. It would help us"
                      " improve the study if you could tell us the main reason"
                      " you do not want to participate in this study?"),
        max_length=50,
        choices=WHYNOPARTICIPATE_CHOICE,
        help_text="",
        )
    why_no_participate_other = OtherCharField()

    subject_refusal_status = models.CharField(
        verbose_name="Refusal status",
        max_length=50,
        help_text=("Change the refusal status from 'refused' to 'no longer refusing' if and"
                   " when the subject changes their mind"),
        default='REFUSED',
        editable=False)

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        null=True,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment'))

    history = AuditTrail()

    def get_registration_datetime(self):
        return self.report_datetime

    def member_status_string(self):
        return 'REFUSED'

    def save(self, *args, **kwargs):
        kwargs['reason'] = 'refuse'
        kwargs['info_source'] = 'subject'
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(SubjectRefusal, self).save(*args, **kwargs)

    class Meta:
        app_label = "bcpp_household_member"
        db_table = 'bcpp_subject_subjectrefusal'
        verbose_name = "Refusal Log"
        verbose_name_plural = "Refusal Log"
        ordering = ['household_member']
