from django.db import models
from bhp_registration.models import RegisteredSubject
from bcpp_survey.models import Survey
from base_household_structure_member_model import BaseHouseholdStructureMemberModel
from bcpp_subject.managers import BaseRegisteredHouseholdStructureMemberModelManager


class BaseRegisteredHouseholdStructureMemberModel(BaseHouseholdStructureMemberModel):

    """ base for membership form models that need a foreignkey to the registered subject and household_structure_member model"""

    registered_subject = models.ForeignKey(
        RegisteredSubject,
        null=True
        )
    survey = models.ForeignKey(Survey, editable=False)

    objects = BaseRegisteredHouseholdStructureMemberModelManager()

    def is_dispatchable(self):
        return True

    def __unicode__(self):
        return self.household_structure_member

    def get_registration_datetime(self):
        return self.report_datetime

    def save(self, *args, **kwargs):
        if 'reason' in kwargs:
            # remove two extra keys
            del kwargs['reason']
            del kwargs['info_source']
#         if not self.registered_subject and self.household_structure_member.registered_subject:
#             self.registered_subject = self.household_structure_member.registered_subject
        super(BaseRegisteredHouseholdStructureMemberModel, self).save(*args, **kwargs)

    def confirm_registered_subject_pk_on_post_save(self):
        if self.registered_subject.pk != self.household_structure_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_structure_member.registered_subject.pk. Got {0} != {1}.'.format(self.registered_subject.pk, self.household_structure_member.registered_subject.pk))

    class Meta:
        ordering = ['household_structure_member']
        abstract = True
