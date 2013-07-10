from django.db import models
from bhp_registration.models import RegisteredSubject
from bhp_botswana.models import BaseBwConsent
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey
from subject_off_study_mixin import SubjectOffStudyMixin


class BaseSubjectConsent(SubjectOffStudyMixin, BaseBwConsent):

    registered_subject = models.ForeignKey(RegisteredSubject, editable=False)

    household_member = models.OneToOneField(HouseholdMember)

    survey = models.ForeignKey(Survey)

    is_signed = models.BooleanField(
        default=False
        )

    def __unicode__(self):
        return self.subject_identifier

    def get_registration_datetime(self):
        return self.consent_datetime

    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    def post_save_update_hsm_status(self, **kwargs):
        using = kwargs.get('using', None)
        hsm = self.household_member
        hsm.member_status = 'CONSENTED'
        hsm.save(using=using)
        rs = self.registered_subject
        rs.registration_status = 'consented'
        rs.save(using=using)
        if self.registered_subject.pk != self.household_member.registered_subject.pk:
            raise TypeError('Expected self.registered_subject.pk == self.household_member.registered_subject.pk. Got {0} != {1}.'.format(self.registered_subject.pk, self.household_member.registered_subject.pk))

    def dispatch_container_lookup(self, using=None):
        return (('bcpp_household', 'household'), 'household_member__household_structure__household__household_identifier')

    def household_structure(self):
        return unicode(self.household_member.household_structure)

    def hiv_result(self):
        #return hiv_result.household_hiv_result_option
        return self.subject_hiv_result__household_hiv_result_option

    def art_status(self):
        if self.subject_hiv_result.household_hiv_result_option.result_option == 'A':
            art_status = "N/A"
        else:
            art_status = self.subject_art_history.art_status
        return art_status

    def calendar_absolute_url(self):
        return "/admin%s" % self.get_absolute_url()

    def calendar_datetime(self):
        return self.consent_datetime

    def calendar_label(self):
        return '%s: %s [%s]' % (self.__unicode__(), self.first_name, self.initials)

    class Meta:
        abstract = True
