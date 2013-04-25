from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_registration.models import RegisteredSubject
from base_subject_consent import BaseSubjectConsent
from bhp_common.choices import YES_NO


class BaseSubjectConsentYearX(BaseSubjectConsent):

    screening_datetime = models.DateTimeField(null=True)
    registration_datetime = models.DateTimeField(null=True)
    registration_status = models.CharField(max_length=25, null=True)
    randomization_datetime = models.DateTimeField(null=True)
    is_minor = models.CharField(
        verbose_name="Is subject a minor?",
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text='Subject is a minor if aged 16-17. A guardian must be present for consent. HIV status may NOT be revealed in the household.')

    def deserialize_get_missing_fk(self, attrname):
        if attrname == 'household_structure_member':
            registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_identifier)
            survey = self.survey
            internal_identifier = registered_subject.registration_identifier
            household_structure_member = self.household_structure_member.__class__.objects.get(
                internal_identifier=internal_identifier,
                survey=survey)
            retval = household_structure_member
        else:
            retval = None
        return retval

    def get_subject_type(self):
        return 'subject'

    class Meta:
        abstract = True


class SubjectConsentYearOne(BaseSubjectConsentYearX):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectconsentyearone_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Consent Yr1"
        verbose_name_plural = "Consent Yr1"
        unique_together = (("first_name", "last_name", "dob"),)
        ordering = ['-created']
        


class SubjectConsentYearTwo(BaseSubjectConsentYearX):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectconsentyeartwo_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Consent Yr2"
        verbose_name_plural = "Consent Yr2"
        unique_together = (("first_name", "last_name", "dob"),)
        ordering = ['-created']
        

class SubjectConsentYearThree(BaseSubjectConsentYearX):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectconsentyearthree_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Consent Yr3"
        verbose_name_plural = "Consent Yr3"
        unique_together = (("first_name", "last_name", "dob"),)
        ordering = ['-created']


class SubjectConsentYearFour(BaseSubjectConsentYearX):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectconsentyearfour_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Consent Yr4"
        verbose_name_plural = "Consent Yr4"
        unique_together = (("first_name", "last_name", "dob"),)
        ordering = ['-created']      


class SubjectConsentYearFive(BaseSubjectConsentYearX):

    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectconsentyearfive_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Consent Yr5"
        verbose_name_plural = "Consent Yr5"
        unique_together = (("first_name", "last_name", "dob"),)
        ordering = ['-created']      
