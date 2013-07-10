from django.db import models
from bhp_registration.models import RegisteredSubject
from bcpp_survey.models import Survey
from base_household_member_model import BaseHouseholdMemberModel
from bcpp_subject.managers import BaseRegisteredHouseholdMemberModelManager


class BaseRegisteredHouseholdMemberModel(BaseHouseholdMemberModel):

    """ base for membership form models that need a foreignkey to the registered subject and household_member model"""

    registered_subject = models.ForeignKey(
        RegisteredSubject,
        null=True
        )
    survey = models.ForeignKey(Survey, editable=False)

    objects = BaseRegisteredHouseholdMemberModelManager()

    def is_dispatchable(self):
        return True

    def __unicode__(self):
        return self.household_member

    def get_registration_datetime(self):
        return self.report_datetime

    def save(self, *args, **kwargs):
        if 'reason' in kwargs:
            # remove two extra keys
            del kwargs['reason']
            del kwargs['info_source']
#         if not self.registered_subject and self.household_member.registered_subject:
#             self.registered_subject = self.household_member.registered_subject
        super(BaseRegisteredHouseholdMemberModel, self).save(*args, **kwargs)

    def confirm_registered_subject_pk_on_post_save(self):
        if self.registered_subject.pk != self.household_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_member.registered_subject.pk. Got {0} != {1}.'.format(self.registered_subject.pk, self.household_member.registered_subject.pk))

    class Meta:
        ordering = ['household_member']
        abstract = True
