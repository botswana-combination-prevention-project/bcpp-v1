from datetime import datetime
from django.db import models

from edc.subject.registration.models import RegisteredSubject
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future

from apps.bcpp_survey.models import Survey
from apps.bcpp_subject.managers import BaseRegisteredHouseholdMemberModelManager
from apps.bcpp_household.models import BaseReplacement, Plot

from .household_member import HouseholdMember


class BaseRegisteredHouseholdMemberModel(BaseReplacement):

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
        #return (self.report_datetime, ) + self.household_member.natural_key()
        return self.household_member.natural_key()  # OneToOne field with household_member, so it should be enough alone
    natural_key.dependencies = ['bcpp_household_member.householdmember', ]

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'household_member__household_structure__household__plot__plot_identifier')

    def dispatch_item_container_reference(self, using=None):
        return (('bcpp_household', 'plot'), 'household_structure__household__plot')

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
