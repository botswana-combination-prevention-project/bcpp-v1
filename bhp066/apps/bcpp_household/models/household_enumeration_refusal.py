from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.core.crypto_fields.fields import EncryptedTextField, EncryptedCharField
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from .household import Household
from .plot import Plot
from ..managers import HouseholdRefusalManager


HOUSEHOLD_ENUMERATION_REFUSAL = (
    ('Not Interested', 'Not Interested'),
    ('Does not have time', 'Does not have time'),
    ('Dont want to answer', 'Dont want to answer'),
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
        null=True,
        blank=False
        )

    comment = EncryptedTextField(
        max_length=250,
        null=True,
        blank=False)

    history = AuditTrail()

    objects = HouseholdRefusalManager()

    def natural_key(self):
        return self.household.natural_key()

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household__plot__plot_identifier')

    def __unicode__(self):
        return unicode(self.household) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['household', ]
