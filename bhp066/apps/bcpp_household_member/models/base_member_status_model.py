from django.db import models

from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.registration.models import RegisteredSubject

from bhp066.apps.bcpp_household.models import Plot
from bhp066.apps.bcpp_survey.models import Survey

from ..managers import BaseMemberStatusManager

from .household_member import HouseholdMember


class BaseMemberStatusModel(BaseDispatchSyncUuidModel):

    """ Base for membership form models that need a foreignkey to
    the registered subject and household_member model"""

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        auto_now=False)

    survey = models.ForeignKey(Survey, editable=False)

    objects = BaseMemberStatusManager()

    def __unicode__(self):
        return '{0} {1}'.format(
            self.household_member.member_status.lower(),
            self.get_report_datetime().strftime('%Y-%m-%d'))

    def get_report_datetime(self):
        return self.report_datetime

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_member__household_structure__household__plot')

    def natural_key(self):
        return self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_member__household_structure__household__plot__plot_identifier')

    def is_dispatchable(self):
        return True

    def get_registration_datetime(self):
        return self.report_datetime

    def confirm_registered_subject_pk_on_post_save(self, using):
        if self.registered_subject.pk != self.household_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_member.'
                            'registered_subject.pk. Got {0} != {1}.'.format(
                                self.registered_subject.pk, self.household_member.registered_subject.pk))

    class Meta:
        ordering = ['household_member']
        abstract = True
