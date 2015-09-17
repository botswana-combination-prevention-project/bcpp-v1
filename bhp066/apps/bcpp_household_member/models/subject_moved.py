from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.choices import YES_NO_UNKNOWN
from edc.core.crypto_fields.fields import EncryptedTextField

from bhp066.apps.bcpp_household.exceptions import AlreadyReplaced

from .base_member_status_model import BaseMemberStatusModel


class SubjectMoved(BaseMemberStatusModel):

    moved_household = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the household where last seen',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=False,
        help_text=""
    )

    moved_community = models.CharField(
        max_length=7,
        verbose_name='Has the participant moved out of the community',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=False,
        help_text=""
    )

    new_community = models.CharField(
        max_length=50,
        verbose_name='If the participant has moved, provide the name of the new community',
        null=True,
        blank=True,
        help_text="If moved out of the community, provide a new community name or \'UNKNOWN\'"
    )

    update_locator = models.CharField(
        max_length=7,
        verbose_name='Has the locator information changed',
        choices=YES_NO_UNKNOWN,
        null=True,
        blank=False,
        help_text=('If YES, please enter the changed information '
                   'the locator form')
    )

    comment = EncryptedTextField(
        verbose_name=_("Comment"),
        max_length=250,
        blank=True,
        help_text=('')
    )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(
            household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
        self.survey = self.household_member.survey
        super(SubjectMoved, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_household_member'
        verbose_name = "Subject Moved"
        verbose_name_plural = "Subject Moved"
        ordering = ['household_member']
