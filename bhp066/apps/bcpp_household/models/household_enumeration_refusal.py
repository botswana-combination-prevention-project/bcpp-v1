from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.core.crypto_fields.fields import EncryptedTextField, EncryptedCharField
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from .household import Household


HOUSEHOLD_ENUMERATION_REFUSAL = (
    ('reason1', 'reason one'),
    ('reason2', 'reason two'),
    ('reason3', 'reason three'),
    ('reason4', 'reason four'),
    ('reason5', 'reason five'),
    ('OTHER', 'Other'),
)


class HouseholdEnumerationRefusal(BaseDispatchSyncUuidModel):

    household = models.OneToOneField(Household)

    report_datetime = models.DateTimeField()

    reason = models.CharField(
        verbose_name=_('Please indicate the reason the household cannot be enumerated'),
        max_length=25,
        choices=HOUSEHOLD_ENUMERATION_REFUSAL)

    reason_other = EncryptedCharField(
        verbose_name=_('If Other, specify'),
        max_length=100,
        )

    comment = EncryptedTextField(max_length=250)

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['household', ]
