from datetime import datetime

from edc.constants import YES
from edc.subject.registration.models import RegisteredSubject

from apps.bcpp_household_member.models import HouseholdMember, SubjectHtc
from apps.bcpp_subject.models import SubjectConsent, SubjectReferral

from .bhs_base_export import BaseExport


class Subject(BaseExport):

    def __init__(self, household_member):
        self.instance_datetime = datetime.today()
        super(Subject, self).__init__()
        self.consent_datetime = None
        self.date_of_birth = None
        self.identity = None
        self.identity_type = None
        self.last_name = None
        self.referral_clinic = None
        self.referral_code = None
        self.referral_date = None
        self.subject_accepted_htc = None
        self.subject_consent = None
        self.subject_htc = None
        self.subject_offered_htc = None
        self.subject_referral = None
        self.subject_referred = None
        self.survey_consented = None
        self.household_member = household_member
        self.household_identifier = self.household_member.household_structure.household.household_identifier
        self.plot_identifier = self.household_member.household_structure.household.plot.plot_identifier
        self.gps_lat = self.household_member.household_structure.household.plot.gps_lat
        self.gps_lon = self.household_member.household_structure.household.plot.gps_lat
        self.first_name = self.household_member.first_name
        self.gender = self.household_member.gender
        self.internal_identifier = self.household_member.internal_identifier
        self.created_datetime = self.household_member.created
        self.modified_datetime = self.household_member.modified
        self.household_membership = HouseholdMember.objects.filter(
            internal_identifier=household_member.internal_identifier).order_by('created')
        self.registered_subject = RegisteredSubject.objects.get(
            registration_identifier=self.household_member.internal_identifier)
        self.subject_identifier = self.registered_subject.subject_identifier
        self.surveys = [hm.household_structure.survey.survey_slug for hm in self.household_membership]
        try:
            self.subject_consent = SubjectConsent.objects.get(subject_identifier=self.subject_identifier)
            self.household_member = self.subject_consent.household_member  # set to consented member
            self.internal_identifier = self.household_member.internal_identifier
            self.modified_datetime = self.subject_consent.consent_datetime
            self.age_in_years = self.subject_consent.age
            self.consent_datetime = self.subject_consent.consent_datetime
            self.date_of_birth = self.subject_consent.dob
            self.first_name = self.subject_consent.first_name
            self.gender = self.subject_consent.gender
            self.identity = self.subject_consent.identity
            self.identity_type = self.subject_consent.identity_type
            self.last_name = self.subject_consent.last_name
            self.survey_consented = self.subject_consent.household_member.survey.survey_slug
        except SubjectConsent.DoesNotExist:
            self.age_in_years = self.household_member.age_in_years
        try:
            self.subject_referral = SubjectReferral.objects.get(
                subject_visit__household_member=self.household_member)
            self.subject_referred = self.subject_referral.subject_referred
            if self.subject_referred == YES:
                self.referral_date = self.subject_referral.referral_appt_date
                self.referral_code = self.subject_referral.referral_code
                self.referral_clinic = self.subject_referral.referral_clinic
        except SubjectReferral.DoesNotExist:
            pass
        try:
            self.subject_htc = SubjectHtc.objects.get(household_member=self.household_member)
            self.subject_offered_htc = self.subject_htc.offered
            self.subject_accepted_htc = self.subject_htc.accepted
            self.subject_referred = self.subject_htc.referred
            self.referral_code = '_HTC'
            self.referral_clinic = self.subject_htc.referral_clinic
            self.subject_identifier = self.subject_htc.tracking_identifier
        except SubjectHtc.DoesNotExist:
            pass

    @property
    def unique_key(self):
        return self.internal_identifier

    def __repr__(self):
        return 'BhsSubjectHelper({})'.format(self.household_member)

    def __str__(self):
        return '{0.household_member}'.format(self)
