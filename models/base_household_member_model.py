from datetime import datetime
from django.db import models
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bcpp_household.models import Household
from bcpp_household_member.models import HouseholdMember
from base_uuid_model import BaseUuidModel
from bcpp_subject.managers import BaseHouseholdMemberModelManager


class BaseHouseholdMemberModel(BaseUuidModel):

    """ base for models that need a foreignkey to the household_member model"""

    household_member = models.OneToOneField(HouseholdMember)
    report_datetime = models.DateTimeField("Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today())

    objects = BaseHouseholdMemberModelManager()

    def __unicode__(self):
        return self.household_member

    def natural_key(self):
        return (self.report_datetime, ) + self.household_member.natural_key()
    natural_key.dependencies = ['mochudi_household.householdmember', ]

    def dispatch_container_lookup(self, using=None):
        return (Household, 'household_member__household_structure__household__household_identifier')

    def dispatch_item_container_reference(self, using=None):
        return (('mochudi_household', 'household'), 'household_structure__household')

    class Meta:
        ordering = ['household_member']
        abstract = True
