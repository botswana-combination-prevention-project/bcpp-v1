import re
import uuid

from datetime import date
from dateutil.relativedelta import relativedelta

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from edc.core.bhp_common.utils import formatted_age
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc_base.audit_trail import AuditTrail
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_consent.models.fields import (ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
                                       SampleCollectionFieldsMixin, CitizenFieldsMixin)
from edc_constants.constants import YES, NO

from bhp066.apps.bcpp_household_member.constants import BHS_ELIGIBLE, BHS
from bhp066.apps.bcpp_household_member.models import EnrollmentChecklist
from bhp066.apps.bcpp_household_member.exceptions import MemberStatusError

from ..exceptions import ConsentError
from ..managers import SubjectConsentManager

from .base_household_member_consent import BaseHouseholdMemberConsent, BaseSyncHouseholdMemberConsent
from .subject_off_study_mixin import SubjectOffStudyMixin


class BaseBaseSubjectConsent(BaseHouseholdMemberConsent):

    def save(self, *args, **kwargs):
        self.insert_dummy_identifier()
        if not self.id:
            self._save_new_consent(kwargs.get('using', None))
        self.subject_type = self.get_subject_type()
        super(BaseBaseSubjectConsent, self).save(*args, **kwargs)

    def save_new_consent(self, using=None, subject_identifier=None):
        """ Users may override this to compliment the default behavior for new instances.

        Must return a subject_identifier or None."""

        return subject_identifier

    def _save_new_consent(self, using=None, **kwargs):
        from ..classes import ConsentedSubjectIdentifier
        """ Creates or gets a subject identifier.

        ..note:: registered subject is updated/created on edc.subject signal.

        Also, calls user method :func:`save_new_consent`"""
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
                try:
                    self.subject_identifier = self.registered_subject.subject_identifier
                except AttributeError:
                    pass
            # create a subject identifier, if not already done
            if re_pk.match(self.subject_identifier):
                consented_subject_identifier = ConsentedSubjectIdentifier(site_code=self.get_site_code(), using=using)
                self.subject_identifier = consented_subject_identifier.get_identifier(using=using)
        if not self.subject_identifier:
            self.subject_identifier = dummy
        if re_pk.match(self.subject_identifier):
            raise ConsentError("Subject identifier not set after saving new consent! Got {0}".format(self.subject_identifier))

    def insert_dummy_identifier(self):
        """Inserts a random uuid as a dummy identifier for a new instance.

        Model uses subject_identifier_as_pk as a natural key for
        serialization/deserialization. Value must not change once set."""

        # set to uuid if new and not specified
        if not self.id:
            subject_identifier_as_pk = str(uuid.uuid4())
            self.subject_identifier_as_pk = subject_identifier_as_pk  # this will never change
            if not self.subject_identifier:
                # this will be changed when allocated a subject_identifier on consent
                self.subject_identifier = subject_identifier_as_pk
        # never allow subject_identifier as None
        if not self.subject_identifier:
            raise ConsentError('Subject Identifier may not be left blank.')
        # never allow subject_identifier_as_pk as None
        if not self.subject_identifier_as_pk:
            raise ConsentError('Attribute subject_identifier_as_pk on model '
                               '{0} may not be left blank. Expected to be set '
                               'to a uuid already.'.format(self._meta.object_name))

    def _get_user_provided_subject_identifier(self):
        """Return a user provided subject_identifier.

        Do not override."""
        if self.get_user_provided_subject_identifier_attrname() in dir(self):
            return getattr(self, self.get_user_provided_subject_identifier_attrname())
        else:
            return None

    def get_user_provided_subject_identifier_attrname(self):
        """Override to return the attribute name of the user provided subject_identifier."""
        return None

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
    def age_at_consent(self):
        age_in_years = relativedelta(self.consent_datetime, self.dob).years
        return age_in_years

    class Meta:
        abstract = True


class BaseSubjectConsent(SubjectOffStudyMixin, BaseSyncHouseholdMemberConsent, BaseBaseSubjectConsent):

    def matches_hic_enrollment(self, subject_consent, household_member, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        HicEnrollment = models.get_model('bcpp_subject', 'HicEnrollment')
        if HicEnrollment.objects.filter(subject_visit__household_member=household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=household_member)
            # consent_datetime does not exist in cleaned_data as it not editable.
            # if subject_consent.dob != hic_enrollment.dob or
            # subject_consent.consent_datetime != hic_enrollment.consent_datetime:
            if subject_consent.dob != hic_enrollment.dob:
                raise exception_cls('An HicEnrollment form already exists for this '
                                    'Subject. So \'dob\' cannot be changed.')

    def matches_enrollment_checklist(self, subject_consent, exception_cls=None):
        """Matches values in this consent against the enrollment checklist.

        ..note:: the enrollment checklist is required for consent, so always exists."""
        # enrollment checklist is only filled for the same survey as the consent
        household_member = self.household_member
        exception_cls = exception_cls or ValidationError
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member__registered_subject=subject_consent.household_member.registered_subject, is_eligible=True)
            household_member = enrollment_checklist.household_member
        except EnrollmentChecklist.DoesNotExist:
            raise exception_cls(
                'A valid Enrollment Checklist not found (is_eligible). The Enrollment Checklist is required before consent.')
        if enrollment_checklist.dob != subject_consent.dob:
            raise exception_cls('Dob does not match that on the enrollment checklist')
        if enrollment_checklist.initials != subject_consent.initials:
            raise exception_cls('Initials do not match those on the enrollment checklist')
        if subject_consent.consent_datetime:
            if subject_consent.minor:
                if (enrollment_checklist.guardian == YES and
                        not (subject_consent.minor and subject_consent.guardian_name)):
                    raise exception_cls('Enrollment Checklist indicates that subject is a minor with guardian '
                                        'available, but the consent does not indicate this.')
        if enrollment_checklist.gender != subject_consent.gender:
            raise exception_cls('Gender does not match that in the enrollment checklist')
        if enrollment_checklist.citizen != subject_consent.citizen:
            raise exception_cls(
                'You wrote subject is a %(citizen)s citizen. This does not match the enrollment checklist.',
                params={"citizen": '' if subject_consent.citizen == YES else 'NOT'})
        if (enrollment_checklist.literacy == YES and
                not (subject_consent.is_literate == YES or (subject_consent.is_literate == NO) and
                     subject_consent.witness_name)):
            raise exception_cls('Answer to whether this subject is literate/not literate but with a '
                                'literate witness, does not match that in enrollment checklist.')
        if ((enrollment_checklist.legal_marriage == YES and
                enrollment_checklist.marriage_certificate == YES) and not (
                subject_consent.legal_marriage == YES and
                subject_consent.marriage_certificate == YES)):
            raise exception_cls('Enrollment Checklist indicates that this subject is married '
                                'to a citizen with a valid marriage certificate, but the '
                                'consent does not indicate this.')
        if not household_member.eligible_subject:
            raise exception_cls('Subject is not eligible or has not been confirmed eligible '
                                'for BHS. Perhaps catch this in the forms.py. Got {0}'.format(household_member))
        return True

    def get_hiv_status(self):
        """Returns the hiv testing history as a string.

        .. note:: more than one table is tracked so the history includes HIV results not performed by our team
                  as well as the results of tests we perform."""
        return site_lab_tracker.get_history_as_string('HIV', self.subject_identifier, 'subject')

    @property
    def survey_of_consent(self):
        return self.survey.survey_name

    @property
    def minor(self):
        age_at_consent = relativedelta(
            date(self.consent_datetime.year,
                 self.consent_datetime.month,
                 self.consent_datetime.day),
            self.dob).years
        return age_at_consent >= 16 and age_at_consent <= 17

    @property
    def age(self):
        return relativedelta(self.consent_datetime, self.dob).years

    def formatted_age_at_consent(self):
        return formatted_age(self.dob, self.consent_datetime)

    @classmethod
    def get_consent_update_model(self):
        raise TypeError('The ConsentUpdateModel is required. Specify a class method get_consent_update_model() on the model to return the ConsentUpdateModel class.')

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

#     def update_consent_history(self, created, using):
#         from edc.subject.consent.models import BaseConsentHistory
#         """Updates the consent history model for this consent instance if there is a consent history model."""
#         if self.get_consent_history_model():
#             if not issubclass(self.get_consent_history_model(), BaseConsentHistory):
#                 raise ImproperlyConfigured('Expected a subclass of BaseConsentHistory.')
#             self.get_consent_history_model().objects.update_consent_history(self, created, using)
#
#     def delete_consent_history(self, app_label, model_name, pk, using):
#         from edc.subject.consent.models import BaseConsentHistory
#         if self.get_consent_history_model():
#             if not issubclass(self.get_consent_history_model(), BaseConsentHistory):
#                 raise ImproperlyConfigured('Expected a subclass of BaseConsentHistory.')
#             self.get_consent_history_model().objects.delete_consent_history(app_label, model_name, pk, using)

    def include_for_dispatch(self):
        return True

    def dispatch_container_lookup(self, using=None):
        return (models.get_model('bcpp_household', 'Plot'),
                'household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        consents = self.__class__.objects.filter(
            household_member__internal_identifier=self.household_member.internal_identifier).exclude(
            household_member=self.household_member)
        if not consents.exists():
            if not self.id:
                expected_member_status = BHS_ELIGIBLE
            else:
                expected_member_status = BHS
            subject_identifier = self.household_member.get_subject_identifier()
            try:
                self.__class__.objects.filter(subject_identifier=subject_identifier).latest('consent_datetime')
                expected_member_status = BHS
                self.subject_identifier = subject_identifier
            except ObjectDoesNotExist:
                pass
            if self.household_member.member_status != expected_member_status:
                raise MemberStatusError('Expected member status to be {0}. Got {1} for {2}.'.format(
                    expected_member_status, self.household_member.member_status, self.household_member))
            self.is_minor = YES if self.minor else NO
            self.matches_enrollment_checklist(self)
            self.matches_hic_enrollment(self, self.household_member)
        else:
            self.registered_subject = consents[0].registered_subject
            self.subject_identifier = consents[0].subject_identifier
        self.community = self.household_member.household_structure.household.plot.community
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SubjectConsent(IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
                     SampleCollectionFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin,
                     BaseSubjectConsent):

    """ A model completed by the user that captures the ICF."""

    objects = SubjectConsentManager()

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'survey', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )


class SubjectConsentExtended(SubjectConsent):

    """ A system model that serves as a proxy model for SubjectConsent."""

    SUBJECT_TYPES = ['subject']
    GENDER_OF_CONSENT = ['M', 'F']
    AGE_IS_ADULT = 18
    MIN_AGE_OF_CONSENT = 16
    MAX_AGE_OF_CONSENT = 120

    class Meta:
        proxy = True
        get_latest_by = 'consent_datetime'
        app_label = 'bcpp_subject'
