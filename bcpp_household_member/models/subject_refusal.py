from django.db import models

from simple_history.models import HistoricalRecords

from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future

from ..choices import WHY_NOPARTICIPATE_CHOICE
from ..managers import HouseholdMemberManager

from .model_mixins import HouseholdMemberModelMixin


class SubjectRefusal (HouseholdMemberModelMixin):
    """A model completed by the user that captures reasons for a
    potentially eligible household member refusing participating in BHS."""
    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_future],
        help_text="Date format is YYYY-MM-DD")

    reason = models.CharField(
        verbose_name="We respect your decision to decline. It would help us"
                     " improve the study if you could tell us the main reason"
                     " you do not want to participate in this study?",
        max_length=50,
        choices=WHY_NOPARTICIPATE_CHOICE,
        help_text="")

    reason_other = OtherCharField()

    subject_refusal_status = models.CharField(
        verbose_name="Refusal status",
        max_length=100,
        help_text="Change the refusal status from 'refused' to 'no longer refusing' if and"
                  " when the subject changes their mind",
        default='REFUSED',
        editable=False)

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        null=True,
        blank=True,
        help_text='IMPORTANT: Do not include any names or other personally identifying '
                  'information in this comment')

    objects = HouseholdMemberManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
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

    class Meta(HouseholdMemberModelMixin.Meta):
        app_label = "bcpp_household_member"
        verbose_name = "Subject Refusal"
        verbose_name_plural = "Subject Refusal"
