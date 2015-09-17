import re

from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import eligible_if_yes
from edc.choices.common import YES_NO, YES_NO_NA
from edc.constants import NOT_APPLICABLE
from edc.map.classes import site_mappers
from edc.core.bhp_common.utils import formatted_age
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_consent.models.fields import (ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
                                       SampleCollectionFieldsMixin)
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.core.bhp_variables.models import StudySite
# from edc.subject.consent.exceptions import ConsentError
# from edc.subject.consent.classes import ConsentedSubjectIdentifier

from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_household_member.constants import BHS_ELIGIBLE, BHS
from bhp066.apps.bcpp_household_member.models import EnrollmentChecklist
from bhp066.apps.bcpp_household_member.exceptions import MemberStatusError

from ..managers import SubjectConsentManager

from .base_household_member_consent import BaseHouseholdMemberConsent
from .hic_enrollment import HicEnrollment
from .subject_consent_history import SubjectConsentHistory
from .subject_off_study_mixin import SubjectOffStudyMixin


class BaseSubjectConsent(SubjectOffStudyMixin, BaseHouseholdMemberConsent):

    study_site = models.ForeignKey(
        StudySite,
        verbose_name='Site',
        null=True,
        help_text="This refers to the site or 'clinic area' where the subject is being consented."
    )

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        help_text="",
    )

    legal_marriage = models.CharField(
        verbose_name=("If not a citizen, are you legally married to a Botswana Citizen?"),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant will not be enrolled.",
    )

    marriage_certificate = models.CharField(
        verbose_name=("[Interviewer] Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO_NA,
        null=True,
        blank=False,
        default=NOT_APPLICABLE,
        help_text="If 'NO' participant will not be enrolled.",
    )

    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY",
    )

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'))

    consent_signature = models.CharField(
        verbose_name=("The client has signed the consent form?"),
        max_length=3,
        choices=YES_NO,
        validators=[eligible_if_yes, ],
        null=True,
        blank=False,
        # default='Yes',
        help_text="If no, INELIGIBLE",
    )

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    def save(self, *args, **kwargs):
        # From old edc BaseConsent
        if not self.id:
            self._save_new_consent(kwargs.get('using', None))
        # From old edc BaseSubject
        self.subject_type = self.get_subject_type()
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    def matches_hic_enrollment(self, subject_consent, household_member, exception_cls=None):
        exception_cls = exception_cls or ValidationError

        if HicEnrollment.objects.filter(subject_visit__household_member=household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=household_member)
            # consent_datetime does not exist in cleaned_data as it not editable.
            # if subject_consent.dob != hic_enrollment.dob or
            # subject_consent.consent_datetime != hic_enrollment.consent_datetime:
            if subject_consent.dob != hic_enrollment.dob:
                raise exception_cls('An HicEnrollment form already exists for this '
                                    'Subject. So \'dob\' cannot be changed.')

    def matches_enrollment_checklist(self, subject_consent, household_member, exception_cls=None):
        """Matches values in this consent against the enrollment checklist.

        ..note:: the enrollment checklist is required for consent, so always exists."""
        # enrollment checklist is only filled for the same survey as the consent
        household_member = subject_consent.household_member
        exception_cls = exception_cls or ValidationError
        if not EnrollmentChecklist.objects.filter(household_member=household_member).exists():
            raise exception_cls('Enrollment Checklist not found. The Enrollment Checklist is required before consent.')
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        if enrollment_checklist.dob != subject_consent.dob:
            raise exception_cls('Dob does not match that on the enrollment checklist')
        if enrollment_checklist.initials != subject_consent.initials:
            raise exception_cls('Initials do not match those on the enrollment checklist')
        if (enrollment_checklist.guardian.lower() == 'yes' and
                not (subject_consent.minor and subject_consent.guardian_name)):
            raise exception_cls('Enrollment Checklist indicates that subject is a minor with guardian '
                                'available, but the consent does not indicate this.')
        if enrollment_checklist.gender != subject_consent.gender:
            raise exception_cls('Gender does not match that in the enrollment checklist')
        if enrollment_checklist.citizen != subject_consent.citizen:
            raise exception_cls(
                'Answer to whether this subject a citizen, does not match that in enrollment checklist.')
        if (enrollment_checklist.literacy.lower() == 'yes' and
                not (subject_consent.is_literate.lower() == 'yes' or (subject_consent.is_literate.lower() == 'no') and
                     subject_consent.witness_name)):
            raise exception_cls('Answer to whether this subject is literate/not literate but with a '
                                'literate witness, does not match that in enrollment checklist.')
        if ((enrollment_checklist.legal_marriage.lower() == 'yes' and
                enrollment_checklist.marriage_certificate.lower() == 'yes') and not (
                subject_consent.legal_marriage.lower() == 'yes' and
                subject_consent.marriage_certificate.lower() == 'yes')):
            raise exception_cls('Enrollment Checklist indicates that this subject is married '
                                'to a citizen with a valid marriage certificate, but the '
                                'consent does not indicate this.')
        if not household_member.eligible_subject:
            raise exception_cls('Subject is not eligible or has not been confirmed eligible '
                                'for BHS. Perhaps catch this in the forms.py. Got {0}'.format(household_member))
        return True

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_subject_type(self):
        return 'subject'

    def get_consent_history_model(self):
        return SubjectConsentHistory

    def get_registered_subject(self):
        return self.registered_subject

    def get_hiv_status(self):
        """Returns the hiv testing history as a string.

        .. note:: more than one table is tracked so the history includes HIV results not performed by our team
                  as well as the results of tests we perform."""
        return site_lab_tracker.get_history_as_string('HIV', self.subject_identifier, 'subject')

    @property
    def age_at_consent(self):
        age_in_years = relativedelta(date.today(), self.dob).years
        years_since_consent = relativedelta(date.today(), self.consent_datetime).years
        return age_in_years - years_since_consent

    @property
    def survey_of_consent(self):
        return self.survey.survey_name

    @property
    def minor(self):
        age_at_consent = relativedelta(date(self.consent_datetime.year,
                                            self.consent_datetime.month,
                                            self.consent_datetime.day),
                                       self.dob).years
        return age_at_consent >= 16 and age_at_consent <= 17

    def save_new_consent(self, using=None, subject_identifier=None):
        """ Users may override this to compliment the default behavior for new instances.

        Must return a subject_identifier or None."""

        return subject_identifier

    def _save_new_consent(self, using=None, **kwargs):
        """ Creates or gets a subject identifier.

        ..note:: registered subject is updated/created on edc.subject signal.

        Also, calls user method :func:`save_new_consent`"""
        try:
            registered_subject = getattr(self, 'registered_subject')
        except AttributeError:
            registered_subject = None
        self.subject_identifier = self.save_new_consent(using=using, subject_identifier=self.subject_identifier)
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        dummy = self.subject_identifier
        # recall, if subject_identifier is not set, subject_identifier will be a uuid.
        if re_pk.match(self.subject_identifier):
            # test for user provided subject_identifier field method
            if self.get_user_provided_subject_identifier_attrname():
                self.subject_identifier = self._get_user_provided_subject_identifier()
                if not self.subject_identifier:
                    self.subject_identifier = dummy
            # try to get from registered_subject (was created  using signal in edc.subject)
            if re_pk.match(self.subject_identifier):
                if registered_subject:
                    if registered_subject.subject_identifier:
                        # check for  registered subject key and if it already has
                        # a subject_identifier (e.g for subjects re-consenting)
                        self.subject_identifier = self.registered_subject.subject_identifier
            # create a subject identifier, if not already done
            if re_pk.match(self.subject_identifier):
                consented_subject_identifier = ConsentedSubjectIdentifier(site_code=self.get_site_code(), using=using)
                self.subject_identifier = consented_subject_identifier.get_identifier(using=using)
        if not self.subject_identifier:
            self.subject_identifier = dummy
        if re_pk.match(self.subject_identifier):
            raise ConsentError("Subject identifier not set after saving new consent! Got {0}".format(self.subject_identifier))

    @property
    def registered_subject_options(self):
        """Returns a dictionary of RegisteredSubject attributes
        ({field, value}) to be used, for example, as the defaults
        kwarg RegisteredSubject.objects.get_or_create()."""
        options = {
            'study_site': self.study_site,
            'dob': self.dob,
            'is_dob_estimated': self.is_dob_estimated,
            'gender': self.gender,
            'initials': self.initials,
            'identity': self.identity,
            'identity_type': self.identity_type,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'subject_type': self.get_subject_type(),
        }
        if self.last_name:
            options.update({'registration_status': 'consented'})
        return options

    @property
    def age(self):
        return relativedelta(self.consent_datetime, self.dob).years

    def formatted_age_at_consent(self):
        return formatted_age(self.dob, self.consent_datetime)

    @classmethod
    def get_consent_update_model(self):
        raise TypeError('The ConsentUpdateModel is required. Specify a class method get_consent_update_model() on the model to return the ConsentUpdateModel class.')

    def get_report_datetime(self):
        return self.consent_datetime

    def bypass_for_edit_dispatched_as_item(self, using=None, update_fields=None):
        """Allow bypass only if doing consent verification."""
        # requery myself
        obj = self.__class__.objects.using(using).get(pk=self.pk)
        # dont allow values in these fields to change if dispatched
        may_not_change_these_fields = [(k, v) for k, v in obj.__dict__.iteritems() if k not in ['is_verified_datetime', 'is_verified']]
        for k, v in may_not_change_these_fields:
            if k[0] != '_':
                if getattr(self, k) != v:
                    return False
        return True

    def update_consent_history(self, created, using):
        from edc.subject.consent.models import BaseConsentHistory
        """Updates the consent history model for this consent instance if there is a consent history model."""
        if self.get_consent_history_model():
            if not issubclass(self.get_consent_history_model(), BaseConsentHistory):
                raise ImproperlyConfigured('Expected a subclass of BaseConsentHistory.')
            self.get_consent_history_model().objects.update_consent_history(self, created, using)

    def delete_consent_history(self, app_label, model_name, pk, using):
        from edc.subject.consent.models import BaseConsentHistory
        if self.get_consent_history_model():
            if not issubclass(self.get_consent_history_model(), BaseConsentHistory):
                raise ImproperlyConfigured('Expected a subclass of BaseConsentHistory.')
            self.get_consent_history_model().objects.delete_consent_history(app_label, model_name, pk, using)

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True


class SubjectConsent(IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin, SampleCollectionFieldsMixin,
                     VulnerabilityFieldsMixin, BaseSubjectConsent):

    history = AuditTrail()

    objects = SubjectConsentManager()

    def dispatch_container_lookup(self, using=None):
        return (models.get_model('bcpp_household', 'Plot'),
                'household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        if not self.id:
            expected_member_status = BHS_ELIGIBLE
        else:
            expected_member_status = BHS
        if self.household_member.member_status != expected_member_status:
            raise MemberStatusError('Expected member status to be {0}. Got {1} for {2}.'.format(
                expected_member_status, self.household_member.member_status, self.household_member))
        if self.confirm_identity:
            if self.identity != self.confirm_identity:
                raise ValueError('Attribute \'identity\' must match attribute \'confirm_identity\'. Catch this error on the form')
        self.is_minor = 'Yes' if self.minor else 'No'
        self.matches_enrollment_checklist(self, self.household_member)
        self.matches_hic_enrollment(self, self.household_member)
        self.community = self.household_member.household_structure.household.plot.community
        super(SubjectConsent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        unique_together = (('subject_identifier', 'survey', 'version'), ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
