from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

from edc.audit.audit_trail import AuditTrail
from edc.core.crypto_fields.fields import EncryptedTextField, EncryptedCharField

from ..managers import HouseholdEnumerationRefusalManager
from .household_structure import HouseholdStructure
from .plot import Plot
from .base_replacement import BaseReplacement

HOUSEHOLD_REFUSAL = (
    ('not_interested', 'Not Interested'),
    ('does_not_have_time', 'Does not have time'),
    ('dont_want_to_answer', 'Don\'t want to answer'),
    ('other', 'Other'),
)


class HouseholdEnumerationRefusal(BaseReplacement):

    household_structure = models.OneToOneField(HouseholdStructure)

    report_datetime = models.DateTimeField()

    reason = models.CharField(
        verbose_name=_('Please indicate the reason the household cannot be enumerated'),
        max_length=25,
        choices=HOUSEHOLD_REFUSAL)

    reason_other = EncryptedCharField(
        verbose_name=_('If Other, specify'),
        max_length=100,
        blank=True,
        null=True,
        )

    comment = EncryptedTextField(
        max_length=250,
        help_text=_("You may provide a comment here or leave BLANK."),
        blank=True,
        null=True,
        )

    objects = HouseholdEnumerationRefusalManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        if self.household_structure.enrolled:
            raise ValidationError('Household is enrolled.')
        self.household_structure.refused_enumeration = True
        super(HouseholdEnumerationRefusal, self).save(*args, **kwargs)

    def natural_key(self):
        return self.household_structure.natural_key()
    natural_key.dependencies = ['bcpp_household.household_structure']

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_structure__household__plot__plot_identifier')

    def replacement_container(self, using=None):
        return self.household

    def __unicode__(self):
        return unicode(self.household_structure) + '(' + unicode(self.report_datetime) + ')'

    class Meta:
        app_label = 'bcpp_household'
        ordering = ['household_structure', ]
