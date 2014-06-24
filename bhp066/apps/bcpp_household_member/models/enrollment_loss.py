from django.db import models

from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.base.model.validators import dob_not_future

from apps.bcpp_household_member.constants import BHS_LOSS, BHS_SCREEN, NOT_ELIGIBLE
from apps.bcpp_household_member.exceptions import MemberStatusError
from apps.bcpp_household.exceptions import AlreadyReplaced

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
        household = models.get_model('bcpp_household', 'Household').objects.get(household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
#         if not self.id:
#             if self.household_member.member_status != BHS_SCREEN:
#                 raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(BHS_SCREEN, self.household_member.member_status))
#         else:
        if self.household_member.member_status != NOT_ELIGIBLE:
            raise MemberStatusError('Expected member status to be {0}. Got {1}'.format(NOT_ELIGIBLE, self.household_member.member_status))
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        self.household_member.enrollment_loss_completed = True
        #important during dispatch, need to save instance to the correct db.
        self.household_member.save(using=kwargs.get('using',None))
        super(EnrollmentLoss, self).save(*args, **kwargs)

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
