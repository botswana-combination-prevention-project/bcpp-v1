from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.base.model.validators import dob_not_future

from bhp066.apps.bcpp_household.exceptions import AlreadyReplaced

from ..constants import NOT_ELIGIBLE
from ..exceptions import MemberStatusError
from ..managers import EnrollmentLossManager

from .household_member import HouseholdMember


class EnrollmentLoss(BaseDispatchSyncUuidModel):
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

    history = AuditTrail()

    def save(self, *args, **kwargs):
        household = models.get_model('bcpp_household', 'Household').objects.get(
            household_identifier=self.household_member.household_structure.household.household_identifier)
        if household.replaced_by:
            raise AlreadyReplaced('Household {0} replaced.'.format(household.household_identifier))
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

    def __unicode__(self):
        return str(self.household_member)

    def natural_key(self):
        if not self.household_member:
            raise AttributeError('household_member cannot be None for enrollment loss '
                                 'with pk=\'{0}\''.format(self.pk))
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household.household_member']

    def dispatch_container_lookup(self, using=None):
        return (models.get_model('bcpp_household', 'Plot'),
                'household_member__household_structure__household__plot__plot_identifier')

    def deserialize_prep(self, **kwargs):
        # EnrollmentLoss being deleted by an IncommingTransaction, we go ahead and delete it.
        # Its no longer needed at all because member status changed.
        if kwargs.get('action', None) and kwargs.get('action', None) == 'D':
            self.delete()

    class Meta:
        app_label = 'bcpp_household_member'
