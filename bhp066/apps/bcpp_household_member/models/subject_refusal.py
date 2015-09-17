from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc_base.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import date_not_future, date_not_before_study_start

from bhp066.apps.bcpp.choices import WHYNOPARTICIPATE_CHOICE
from bhp066.apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


class SubjectRefusal (BaseMemberStatusModel):
    """A model completed by the user that captures reasons for a
    potentially eligible household member refusing participating in BHS."""
    refusal_date = models.DateField(
        verbose_name=_("Date subject refused participation"),
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")

    reason = models.CharField(
        verbose_name=_("We respect your decision to decline. It would help us"
                       " improve the study if you could tell us the main reason"
                       " you do not want to participate in this study?"),
        max_length=50,
        choices=WHYNOPARTICIPATE_CHOICE,
        help_text="")

    reason_other = OtherCharField()

    subject_refusal_status = models.CharField(
        verbose_name=_("Refusal status"),
        max_length=100,
        help_text=_("Change the refusal status from 'refused' to 'no longer refusing' if and"
                    " when the subject changes their mind"),
        default='REFUSED',
        editable=False)

    comment = models.CharField(
        verbose_name=_("Comment"),
        max_length=250,
        null=True,
        blank=True,
        help_text=_('IMPORTANT: Do not include any names or other personally identifying '
                    'information in this comment'))

    history = AuditTrail()

    def get_registration_datetime(self):
        return self.report_datetime

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(
            household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        try:
            update_fields = kwargs.get('update_fields') + ['registered_subject', 'survey', ]
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(SubjectRefusal, self).save(*args, **kwargs)

    def deserialize_prep(self, **kwargs):
        # SubjectRefusal being deleted by an IncommingTransaction, we ahead and delete it.
        # Its no longer needed at all because member status changed.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Subject Refusal"
        verbose_name_plural = "Subject Refusal"
        ordering = ['household_member']
