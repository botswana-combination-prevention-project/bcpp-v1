from django.db import models
from audit_trail.audit import AuditTrail
from bhp_registration.models import RegisteredSubject
from bhp_common.choices import YES_NO
from bhp_botswana.models import BaseBwConsent
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey
from subject_off_study_mixin import SubjectOffStudyMixin


class SubjectConsent(SubjectOffStudyMixin, BaseBwConsent):

    household_member = models.OneToOneField(HouseholdMember)
    survey = models.OneToOneField(Survey)
    is_signed = models.BooleanField(default=False)
    registered_subject = models.OneToOneField(RegisteredSubject, editable=False, null=True)

    is_minor = models.CharField(
        verbose_name="Is subject a minor?",
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text='Subject is a minor if aged 16-17. A guardian must be present for consent. HIV status may NOT be revealed in the household.')

    history = AuditTrail()

    def get_subject_type(self):
        return 'subject'

    def __unicode__(self):
        return self.subject_identifier

    def get_registration_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(SubjectConsent, self).save(*args, **kwargs)

    def post_save_update_hsm_status(self, **kwargs):
        using = kwargs.get('using', None)
        self.household_member.member_status = 'consented'
        self.household_member.save(using=using)
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
        app_label = 'bcpp_subject'
