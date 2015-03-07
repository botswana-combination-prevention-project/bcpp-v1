from edc.constants import YES, NOT_APPLICABLE, NO

from apps.bcpp_clinic.models import ClinicConsent
from apps.bcpp_household_member.models import SubjectHtc
from apps.bcpp_subject.models import SubjectConsent, SubjectReferral
from apps.bcpp_subject.models import SubjectLocator, Pima
from apps.bcpp_survey.models import Survey

from .base_helper import BaseHelper
from .member import Member


class Subject(BaseHelper):

    def __init__(self, household_member):
        super(Subject, self).__init__()
        self.household_member = household_member
        self.registered_subject = self.household_member.registered_subject
        self.internal_identifier = self.household_member.internal_identifier
        self.member = Member(self.household_member)
        for survey in Survey.objects.all():
            try:
                setattr(self, '{}_{}'.format('member_status', survey.survey_abbrev),
                        self.member.household_membership_survey.get(survey.survey_slug).member_status)
            except AttributeError:
                setattr(self, '{}_{}'.format('member_status', survey.survey_abbrev), None)
        self.update_plot()
        self.update_household()
        self.update_subject_consent()
        self.update_subject_referral()
        self.update_subject_locator()
        self.update_pima()

    def __repr__(self):
        return '{0}({1.household_member!r})'.format(self.__class__.__name__, self)

    def __str__(self):
        return '{0.household_member!s}'.format(self)

    @property
    def unique_key(self):
        return self.internal_identifier

    def customize_for_csv(self):
        super(Subject, self).customize_for_csv()
        self.data['household_member'] = self.data['household_member'].internal_identifier
        self.data['registered_subject'] = self.data['registered_subject'].registration_identifier
        try:
            self.data['consenting_household_member'] = self.data['consenting_household_member'].internal_identifier
        except AttributeError:
            pass
        del self.data['member']
        del self.data['plot']
        del self.data['subject_consent']

    def update_plot(self):
        self.plot = self.household_member.household_structure.household.plot
        self.plot_identifier = self.plot.plot_identifier if not self.plot.plot_identifier.endswith('-00') else 'clinic'
        self.recruitment_type = 'household_survey' if not self.plot_identifier == 'clinic' else 'clinic'
        self.community = self.plot.community

    def update_household(self):
        self.household_identifier = self.household_member.household_structure.household.household_identifier
        if self.plot_identifier == 'clinic':
            self.household_identifier = None

    def update_subject_consent(self):
        try:
            if self.recruitment_type == 'clinic':
                self.subject_consent = ClinicConsent.objects.get(registered_subject=self.registered_subject)
            else:
                self.subject_consent = SubjectConsent.objects.get(registered_subject=self.registered_subject)
            self.consenting_household_member = self.subject_consent.household_member
            self.age_in_years = self.subject_consent.age
            self.citizen = self.subject_consent.citizen or YES if self.subject_consent.identity_type == 'OMANG' else NO
            self.consent_datetime = self.subject_consent.consent_datetime
            self.date_of_birth = self.subject_consent.dob
            self.first_name = self.subject_consent.first_name
            self.gender = self.subject_consent.gender
            self.identity = self.subject_consent.identity
            self.identity_type = self.subject_consent.identity_type
            self.last_name = self.subject_consent.last_name
            self.spouse_of_citizen = None if NOT_APPLICABLE else self.subject_consent.legal_marriage
            self.subject_identifier = self.subject_consent.subject_identifier
            self.survey_consented = self.subject_consent.household_member.survey.survey_slug
        except SubjectConsent.DoesNotExist:
            self.age_in_years = self.household_member.age_in_years
            self.citizen = None
            self.consent_datetime = None
            self.consenting_household_member = None
            self.date_of_birth = None
            self.first_name = self.household_member.first_name
            self.gender = self.household_member.gender
            self.identity = None
            self.identity_type = None
            self.last_name = None
            self.spouse_of_citizen = None
            self.subject_consent = None
            self.subject_identifier = None
            self.survey_consented = None

    def update_subject_referral(self):
        fieldattrs = [('subject_referred', 'referred'),
                      ('referral_appt_date', 'referral_appt_date'),
                      ('referral_clinic', 'referral_clinic'),
                      ('referral_code', 'referral_code'),
                      ('hiv_result', 'hiv_result'),
                      ('hiv_result', 'hiv_result'),
                      ('hiv_result_datetime', 'hiv_result_date'),
                      ('new_pos', 'new_pos'),
                      ('on_art', 'on_art'),
                      ('pregnant', 'pregnant'),
                      ('circumcised', 'circumcised'),
                      ('permanent_resident', 'permanent_resident'),
                      ('part_time_resident', 'part_time_resident'),
                      ('arv_clinic', 'arv_clinic'),
                      ('arv_documentation', 'arv_documentation'),
                      ('direct_hiv_documentation', 'direct_hiv_documentation'),
                      ('indirect_hiv_documentation', 'indirect_hiv_documentation'),
                      ('verbal_hiv_result', 'verbal_hiv_result'),
                      ('todays_hiv_result', 'todays_hiv_result'),
                      ('last_hiv_result', 'last_hiv_result'),
                      ('last_hiv_result_date', 'last_hiv_result_date'),
                      ]
        model_cls = SubjectReferral
        for survey in Survey.objects.all():
            self._update(
                survey.survey_abbrev, fieldattrs, model_cls,
                'subject_visit__household_member',
                self.member.household_membership_survey.get(survey.survey_slug))

    def update_subject_htc(self, survey):
        fieldattrs = [('referral_clinic', 'subject_htc_referral_clinic'),
                      ('accepted', 'subject_htc_accepted'),
                      ('tracking_identifier', 'subject_htc_reference'),
                      ('offered', 'subject_htc_offered'),
                      ('referred', 'subject_htc_referred')]
        model_cls = SubjectHtc
        self._update(
            survey.survey_abbrev, fieldattrs, model_cls,
            'household_member',
            self.member.household_membership_survey.get(survey.survey_slug))

    def update_subject_locator(self):
        try:
            subject_locator = SubjectLocator.objects.get(registered_subject=self.registered_subject)
            self.home_visit_permission = subject_locator.home_visit_permission
            self.may_follow_up = subject_locator.may_follow_up
        except SubjectLocator.DoesNotExist:
            self.home_visit_permission = None
            self.may_follow_up = None

    def update_pima(self):
        fieldattrs = [('pima_today', 'cd4_tested'),
                      ('cd4_datetime', 'cd4_date'),
                      ('cd4_value', 'cd4_value')]
        model_cls = Pima
        for survey in Survey.objects.all():
            pima = self._update(
                survey.survey_abbrev, fieldattrs, model_cls,
                'subject_visit__household_member',
                self.member.household_membership_survey.get(survey.survey_slug)
                )
            try:
                setattr(self, '{}_{}'.format('cd4_not_tested_reason', survey.survey_abbrev),
                        pima.pima_today_other if not pima.pima_today_other.upper() == 'OTHER' else pima.pima_today_other_other)
            except AttributeError:
                setattr(self, '{}_{}'.format('cd4_not_tested_reason', survey.survey_abbrev), None)
