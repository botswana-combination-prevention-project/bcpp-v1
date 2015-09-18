from django.test import SimpleTestCase
from django.forms import ValidationError

from edc.map.classes import Mapper

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc_constants.constants import NOT_APPLICABLE

from edc.subject.lab_tracker.classes import site_lab_tracker

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey

from ..forms import EnrollmentChecklistForm
from ..models import HouseholdMember


class OtsePlotMapper(Mapper):
    map_area = 'otse'
    map_code = '020'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()


class EligibilityFormTests(SimpleTestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community='test_community3', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)

    def test_returns_cleaned_data(self):
        form = EnrollmentChecklistForm()
        form.cleaned_data = {'citizen': 'Yes',
                             'legal_marriage': NOT_APPLICABLE,
                             'marriage_certificate': NOT_APPLICABLE,
                             'marriage_certificate_no': ''}
        self.assertEqual(form.clean(), form.cleaned_data)

    def test_is_citizen0(self):
        "if citizen, legal marriage info is not applicable"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'Yes',
            'legal_marriage': 'Yes',
            'marriage_certificate': NOT_APPLICABLE,
            'marriage_certificate_no': ''}
        self.assertRaisesMessage(ValidationError, 'Marital status is not applicable, Participant is a citizen.', form.clean)

    def test_is_citizen1(self):
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'Yes',
            'legal_marriage': NOT_APPLICABLE,
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': ''}
        self.assertRaisesMessage(ValidationError, 'Marriage Certificate is not applicable, Participant is a citizen.', form.clean)

    def test_is_citizen2(self):
        "if citizen, marriage info is not applicable"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'Yes',
            'legal_marriage': NOT_APPLICABLE,
            'marriage_certificate': NOT_APPLICABLE,
            'marriage_certificate_no': '123'}
        self.assertRaisesMessage(ValidationError, 'Marriage Certificate Number is not required, Participant is a citizen.', form.clean)

    def test_is_not_citizen1(self):
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': NOT_APPLICABLE,
            'marriage_certificate': NOT_APPLICABLE,
            'marriage_certificate_no': ''}
        self.assertRaises(ValidationError, form.clean)

    def test_is_not_citizen2(self):
        "not eligible if not legally married"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'No',
            'marriage_certificate': NOT_APPLICABLE,
            'marriage_certificate_no': ''}
        self.assertRaisesRegexp(ValidationError, 'not\ eligible', form.clean)

    def test_is_not_citizen3(self):
        "Missing proof of legal marriage"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'Yes',
            'marriage_certificate': 'No',
            'marriage_certificate_no': ''}
        self.assertRaisesRegexp(ValidationError, 'not\ eligible', form.clean)

    def test_is_not_citizen4(self):
        "did not indicate is legally married"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': NOT_APPLICABLE,
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': '123'}
        self.assertRaisesRegexp(ValidationError, 'legally married to a Botswana citizen', form.clean)

    def test_is_not_citizen5(self):
        "did not indicate marriage certificate number"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'Yes',
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': ''}
        self.assertRaisesRegexp(ValidationError, 'marriage certificate number', form.clean)

    def test_is_not_citizen6(self):
        "has all marriage info, returns cleaned data"
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'Yes',
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': '123'}
        self.assertEqual(form.clean(), form.cleaned_data)

    def test_gender_match(self):
        "gender should match between household_member and checklist"
        household_member = HouseholdMember()
        household_member.gender = 'M'
        household_member.first_name = 'Martin'
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'household_member': household_member,
            'gender': 'F'}
        self.assertRaisesRegexp(ValidationError, 'Gender does not match', form.clean)
        self.assertRaisesRegexp(ValidationError, 'Martin', form.clean)

    def test_initial_match(self):
        "initial should match between household_member and checklist"
        household_member = HouseholdMember()
        household_member.initials = 'ME'
        household_member.first_name = 'Martin'
        form = EnrollmentChecklistForm()
        form.cleaned_data = {
            'household_member': household_member,
            'initials': 'EE'}
        self.assertRaisesRegexp(ValidationError, 'Initials do not match', form.clean)
        self.assertRaisesRegexp(ValidationError, 'Martin', form.clean)
