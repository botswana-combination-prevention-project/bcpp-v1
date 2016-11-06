from django.db import models

from simple_history.models import HistoricalRecords

from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import dob_not_future

from ..constants import NOT_ELIGIBLE
from ..exceptions import MemberStatusError
from ..managers import EnrollmentLossManager

from .household_member import HouseholdMember


class EnrollmentLoss(SyncModelMixin, BaseUuidModel):
    """A system model auto created that captures the reason for a present BHS eligible member
    who passes BHS eligibility but is not participating in the BHS."""
    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField(
        validators=[dob_not_future])

    reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Do not include any personal identifiable information.')

    objects = EnrollmentLossManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.household_member.member_status != NOT_ELIGIBLE:
            raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(
                NOT_ELIGIBLE, self.household_member.member_status))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        try:
            update_fields = kwargs.get('update_fields') + ['registered_subject', 'survey', ]
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(EnrollmentLoss, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError('household_member cannot be None for enrollment loss '
                                 'with pk=\'{0}\''.format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    class Meta:
        app_label = 'bcpp_household_member'
