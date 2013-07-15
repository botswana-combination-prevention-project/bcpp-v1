from datetime import datetime
from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bcpp_survey.models import Survey
from bcpp_household.models import Household
from bcpp_household_member.models import HouseholdMember
from bhp_dispatch.models import BaseDispatchSyncUuidModel
from bcpp_subject.managers import BaseRegisteredHouseholdMemberModelManager


class BaseRegisteredHouseholdMemberModel(BaseDispatchSyncUuidModel):

    """ base for membership form models that need a foreignkey to the registered subject and household_member model"""

    registered_subject = models.ForeignKey(
        RegisteredSubject,
        null=True
        )

    household_member = models.OneToOneField(HouseholdMember)

    report_datetime = models.DateTimeField("Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today())

    survey = models.ForeignKey(Survey, editable=False)

    objects = BaseRegisteredHouseholdMemberModelManager()

    def __unicode__(self):
        return self.household_member

    def natural_key(self):
        return (self.report_datetime, ) + self.household_member.natural_key()
    natural_key.dependencies = ['mochudi_household.householdmember', ]

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household_member__household_structure__household__household_identifier')

    def dispatch_item_container_reference(self, using=None):
        return (('mochudi_household', 'household'), 'household_structure__household')

    def is_dispatchable(self):
        return True

    def get_registration_datetime(self):
        return self.report_datetime

    def save(self, *args, **kwargs):
        if 'reason' in kwargs:
            # remove two extra keys
            del kwargs['reason']
            del kwargs['info_source']
        super(BaseRegisteredHouseholdMemberModel, self).save(*args, **kwargs)

    def confirm_registered_subject_pk_on_post_save(self):
        if self.registered_subject.pk != self.household_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_member.registered_subject.pk. Got {0} != {1}.'.format(self.registered_subject.pk, self.household_member.registered_subject.pk))

    class Meta:
        ordering = ['household_member']
        abstract = True
