from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_botswana.models import BaseBwConsent
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey
from subject_off_study_mixin import SubjectOffStudyMixin


class BaseSubjectConsent(SubjectOffStudyMixin, BaseBwConsent):

    household_member = models.OneToOneField(HouseholdMember)
    survey = models.OneToOneField(Survey)
    is_signed = models.BooleanField(default=False)
    registered_subject = models.OneToOneField(RegisteredSubject, editable=False, null=True)

    def __unicode__(self):
        return self.subject_identifier

    def get_registration_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    def post_save_update_hsm_status(self, **kwargs):
        using = kwargs.get('using', None)
        self.household_member.member_status = 'consented'
        self.household_member.save(using=using)
        self.registered_subject.registration_status = 'consented'
        self.registered_subject.save(using=using)
#        if self.registered_subject.pk != self.household_member.registered_subject.pk:
#            raise TypeError('Expected self.registered_subject.pk == self.household_member.registered_subject.pk. Got {0} != {1}.'.format(self.registered_subject.pk, self.household_member.registered_subject.pk))

    def dispatch_container_lookup(self, using=None):
        return (('bcpp_household', 'household'), 'household_member__household_structure__household__household_identifier')

    class Meta:
        abstract = True
