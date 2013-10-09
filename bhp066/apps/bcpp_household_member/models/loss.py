from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO, YES_NO_DWTA, YES_NO_NA
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.base.model.validators import dob_not_future, MinConsentAge, MaxConsentAge
from edc.choices.common import GENDER
from .household_member import HouseholdMember


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

    class Meta:
        app_label = 'bcpp_household_member'
