from django.db import models

from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.base.model.validators import dob_not_future

from .household_member import HouseholdMember
from ..managers import LossManager

class Loss (BaseDispatchSyncUuidModel):

    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField(
        validators=[dob_not_future],
        )

    reason = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Do not include any personal identifiable information.'
        )
    
    objects = LossManager()
    
    def natural_key(self):
        return self.household_member.natural_key()
    
    class Meta:
        app_label = 'bcpp_household_member'
