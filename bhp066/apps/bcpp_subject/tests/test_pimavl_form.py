from django.test import TestCase
from django.utils import timezone
from django.test.utils import override_settings

from datetime import timedelta, datetime

from ..models import PimaVl

from datetime import date
from dateutil.relativedelta import relativedelta


from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
# 
from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.models import Survey
# 
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
# 
from .factories import SubjectConsentFactory, SubjectVisitFactory
# 
# 
# from edc_quota.client.models import Quota
# from edc_quota.client.exceptions import QuotaReachedError

class TestPimaVL(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def setUp(self):
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
        HouseholdMemberFactory(household_structure=self.household_structure)

        self.male_dob = date.today() - relativedelta(years=25)
        self.male_age_in_years = 25
        self.male_first_name = 'ERIK'
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

        self.subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male_T0, study_site=self.study_site,
            gender='M', dob=self.male_dob, first_name=self.male_first_name, initials=self.male_initials)

        self.registered_subject_male = RegisteredSubject.objects.get(
            subject_identifier=self.subject_consent_male.subject_identifier)


        self.appointment_male_T0 = Appointment.objects.get(
            registered_subject=self.registered_subject_male, visit_definition__code='T0')

        self.subject_visit_male_T0 = SubjectVisitFactory(
            appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)

        self.data = {
            'easy_of_use': u'Very easy',
            'modified': datetime(2016, 1, 11, 15, 26, 17),
            'poc_today_vl_other_other': u'Error 2097 (Insufficient Sample)',
            'poc_vl_today': u'No',
            'poc_vl_today_other': u'OTHER',
            'poc_vl_type': u'mobile setting',
            'poc_vl_value': None,
            'quota_pk': u'1',
            'report_datetime': datetime(2016, 1, 11, 15, 26, 17),
            'request_code': None,
            'stability': u'',
            'subject_visit':  self.subject_visit_male_T0.id ,
            'time_of_result': datetime(2016, 1, 11, 15, 25, 53),
            'time_of_test': None,
            'user_created': u'smoyo',
            'user_modified': u'',
        }

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_poc_vl_no_other(self):
        from bhp066.apps.bcpp_subject.forms.pima_vl_form import PimaVlForm
        self.data['poc_vl_today_other'] = None

        poc_vl_form = PimaVlForm(data=self.data)
        try:
            errors = ''.join(poc_vl_form.errors.get('__all__'))
            self.assertIn('If POC VL NOT done today, please explain why not?', errors)
        except TypeError:
            self.assertIn('If POC VL NOT done today, please explain why not?', [])

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_poc_vl_no_other_with_correct_value(self):
        from bhp066.apps.bcpp_subject.forms.pima_vl_form import PimaVlForm
        poc_vl_form = PimaVlForm(data=self.data)
        try:
            errors = ''.join(poc_vl_form.errors.get('__all__'))
            self.assertNotIn('If POC VL NOT done today, please explain why not?', list(errors))
        except TypeError as e:
            pass

