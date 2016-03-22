from django.test import TestCase
from django.test.utils import override_settings

from datetime import datetime
from bhp066.apps.bcpp_clinic.tests.factories.clinic_eligibility_factory import ClinicEligibilityFactory

from datetime import date
from dateutil.relativedelta import relativedelta


from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc_constants.constants import YES

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household_member.classes import EnumerationHelper

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile

from edc_quota.client.models import Quota
from edc_quota.client.exceptions import QuotaReachedError
from edc.map.classes.controller import site_mappers


class TestSubjectConsentForm(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'

    def setUp(self):
        site_mappers.autodiscover()
        from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        survey = Survey.objects.all().order_by('datetime_start')[0]

        self.study_site = StudySite.objects.get(site_code='01')

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)

        self.male_dob = date.today() - relativedelta(years=25)
        self.male_age_in_years = 25
        self.male_first_name = 'ERIK'
        self.male_last_name = 'HIEWAI'
        self.male_initials = "EW"

        self.household_member_male_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure, gender='M',
            age_in_years=self.male_age_in_years, first_name=self.male_first_name,
            initials=self.male_initials
        )

        EnrollmentChecklistFactory(
            household_member=self.household_member_male_T0,
            gender='M',
            citizen='Yes',
            dob=self.male_dob,
            guardian='No',
            initials=self.household_member_male_T0.initials,
            part_time_resident='Yes'
        )
        self.data = {
            'last_name': 'WIZZY', 'is_minor': 'No',
            'witness_name': None, 'is_literate': 'Yes', 'subject_type': 'subject',
            'consent_copy': 'Yes', 'is_verified': False, 'consent_signature': None, 'first_name': 'ERIK',
            'dm_comment': None,
            'is_dob_estimated': None, 'verified_by': None, 'user_modified': u'', 'is_signed': True,
            'subject_identifier_aka': None, 'version': u'4',
            'citizen': 'Yes', 'legal_marriage': u'N/A', 'assessment_score': 'Yes',
            'is_incarcerated': 'No', 'consent_reviewed': 'Yes', 'study_questions': 'Yes',
            'study_site_id': self.study_site.id,
            'may_store_samples': YES,
            'community': u'test_community', 'using': 'default', 'marriage_certificate_no': None,
            'identity': '317918515',
            'confirm_identity': '317918515',
            'identity_type': 'OMANG',
            'language': u'not specified',
            'guardian_name': None, 'gender': 'M',
            'household_member': self.household_member_male_T0.id,
            'marriage_certificate': u'N/A', 'dob': self.male_dob,
            'study_site': self.study_site.id,
            'initials': 'EW',
            'language': 'en',
            'is_dob_estimated': '-',
            'consent_signature': YES,
            'consent_datetime': datetime.today(),
        }

    def test_validate_identity_duplicate(self):
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
        self.clinic_eligibility = ClinicEligibilityFactory(identity='317918515')
        consent_form = SubjectConsentForm(data=self.data)
        self.assertIn(u"Identity already used by another participant. Got '317918515'.",
                      consent_form.errors.get("__all__"))

#     def test_validate_identity_valid(self):
#         from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
#         self.clinic_eligibility = ClinicEligibilityFactory(identity='317918515')
#         self.data['identity'] = '317918514'
#         self.data['confirm_identity'] = '317918514'
#         consent_form = SubjectConsentForm(data=self.data)
#         consent_form.save()
#         self.assertEqual(RegisteredSubject.objects.filter(identity=self.data['identity']).count(), 1)
#
#     def test_validate_identity_valid_bhs_and_ahs(self):
#         """ Test identity on
#         """
#         from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
#         self.data['identity'] = '317918515'
#         self.data['confirm_identity'] = '317918515'
#         consent_form = SubjectConsentForm(data=self.data)
#         consent_form.save()
#         self.assertEqual(RegisteredSubject.objects.filter(identity=self.data['identity']).count(), 1)
#         survey_T0 = Survey.objects.all().order_by('datetime_start')[0]
#         survey_T1 = Survey.objects.all().order_by('datetime_start')[1]
#         enumeration_helper_T3 = EnumerationHelper(self.household_structure.household, survey_T0, survey_T1)
#         enumeration_helper_T3.add_members_from_survey()
#
#         household_member_y2 = HouseholdMember.objects.get(
#             registered_subject__identity='317918515',
#             household_structure__survey=survey_T1
#         )
#         self.data['household_member'] = household_member_y2.id
#         self.data['version'] = 4
#         consent_form = SubjectConsentForm(data=self.data)
#         # print consent_form.errors
#         self.assertIn(u"Form may not be saved. Only data from BCPP Year 1 may be added/changed. "
#                       u"(LIMIT_EDIT_TO_CURRENT_SURVEY)",
#                       consent_form.errors.get("__all__"))
