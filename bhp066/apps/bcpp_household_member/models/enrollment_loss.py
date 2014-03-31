from django.db import models

from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.base.model.validators import dob_not_future

from apps.bcpp_household_member.constants import BHS_LOSS,BHS_SCREEN
from apps.bcpp_household_member.exceptions import MemberStatusError

from .household_member import HouseholdMember
from ..managers import EnrollmentLossManager


class EnrollmentLoss(BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField(
        validators=[dob_not_future],
        )

    reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Do not include any personal identifiable information.'
        )

    objects = EnrollmentLossManager()

    def save(self, *args, **kwargs):
        if not self.id:
            if self.household_member.member_status != BHS_SCREEN:
                raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(BHS_LOSS, self.household_member.member_status))
        else:
            if self.household_member.member_status != BHS_LOSS:
                raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(BHS_LOSS, self.household_member.member_status))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        self.household_member.bhs_loss = True
        self.household_member.save()

    def __unicode__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError("household_member cannot be None for enrollment loss with pk='\{0}\'".format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    def dispatch_container_lookup(self, using=None):
        return (models.get_model('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = 'bcpp_household_member'
