from django.db import models
from bhp_botswana.models import BaseBwConsent
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey
from bhp_appointment_helper.models import BaseAppointmentMixin
from bhp_registration.models import RegisteredSubject


class BaseHouseholdMemberConsent(BaseAppointmentMixin, BaseBwConsent):

    household_member = models.ForeignKey(HouseholdMember,
        help_text='')
    survey = models.ForeignKey(Survey)
    is_signed = models.BooleanField(default=False)
    registered_subject = models.ForeignKey(RegisteredSubject,
        editable=False,
        null=True,
        help_text='one registered subject will be related to one household member for each survey')

    def __unicode__(self):
        return self.subject_identifier

    def get_registration_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        self.registered_subject = self.household_member.registered_subject
        super(BaseHouseholdMemberConsent, self).save(*args, **kwargs)

    def post_save_update_hm_status(self, **kwargs):
        using = kwargs.get('using', None)
        self.household_member.member_status = 'consented'
        self.household_member.save(using=using)
        self.registered_subject.subject_identifier = self.subject_identifier
        self.registered_subject.registration_status = 'consented'
        self.registered_subject.save(using=using)

    def dispatch_container_lookup(self, using=None):
        return (('bcpp_household', 'household'), 'household_member__household_structure__household__household_identifier')

    def deserialize_get_missing_fk(self, attrname):
        if attrname == 'household_member':
            registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
            survey = self.survey
            internal_identifier = registered_subject.registration_identifier
            household_member = self.household_member.__class__.objects.get(
                internal_identifier=internal_identifier,
                survey=survey)
            retval = household_member
        else:
            retval = None
        return retval

    class Meta:
        abstract = True
