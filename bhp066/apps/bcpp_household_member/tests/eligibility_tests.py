from datetime import datetime
from django.test import SimpleTestCase
from django.forms import ValidationError
from edc.map.classes import Mapper, site_mappers
from apps.bcpp_survey.tests.factories import SurveyFactory
#from apps.bcpp_household.tests.factories import PlotFactory

from ..forms import EnrolmentChecklistForm
from ..models import HouseholdMember
#from .factories import HouseholdMemberFactory


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

#site_mappers.register(OtsePlotMapper)


class EligibilityTests(SimpleTestCase):

    def setUp(self):
        self.survey = SurveyFactory()

    def test_returns_cleaned_data(self):
        form = EnrolmentChecklistForm()
        form.cleaned_data = {'citizen': 'Yes',
                             'legal_marriage': 'N/A',
                             'marriage_certificate': 'N/A',
                             'marriage_certificate_no': ''}
        self.assertEqual(form.clean(), form.cleaned_data)

    def test_is_citizen0(self):
        "if citizen, legal marriage info is not applicable"
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'Yes',
            'legal_marriage': 'Yes',
            'marriage_certificate': 'N/A',
            'marriage_certificate_no': ''}
        self.assertRaisesMessage(ValidationError, 'Marital status is not applicable, Participant is a citizen.', form.clean)

    def test_is_citizen1(self):
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'Yes',
            'legal_marriage': 'N/A',
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': ''}
        self.assertRaisesMessage(ValidationError, 'Marriage Certificate is not applicable, Participant is a citizen.', form.clean)

    def test_is_citizen2(self):
        "if citizen, marriage info is not applicable"
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'Yes',
            'legal_marriage': 'N/A',
            'marriage_certificate': 'N/A',
            'marriage_certificate_no': '123'}
        self.assertRaisesMessage(ValidationError, 'Marriage Certificate Number is not required, Participant is a citizen.', form.clean)

    def test_is_not_citizen1(self):
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'N/A',
            'marriage_certificate': 'N/A',
            'marriage_certificate_no': ''}
        self.assertRaises(ValidationError, form.clean)

    def test_is_not_citizen2(self):
        "not eligible if not legally married"
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'No',
            'marriage_certificate': 'N/A',
            'marriage_certificate_no': ''}
        self.assertRaisesRegexp(ValidationError, 'not\ eligible', form.clean)

    def test_is_not_citizen3(self):
        "Missing proof of legal marriage"
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'Yes',
            'marriage_certificate': 'No',
            'marriage_certificate_no': ''}
        self.assertRaisesRegexp(ValidationError, 'not\ eligible', form.clean)

    def test_is_not_citizen4(self):
        "did not indicate is legally married"
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'N/A',
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': '123'}
        self.assertRaisesRegexp(ValidationError, 'legally married to a Botswana citizen', form.clean)

    def test_is_not_citizen5(self):
        "did not indicate marriage certificate number"
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'citizen': 'No',
            'legal_marriage': 'Yes',
            'marriage_certificate': 'Yes',
            'marriage_certificate_no': ''}
        self.assertRaisesRegexp(ValidationError, 'marriage certificate number', form.clean)

    def test_is_not_citizen6(self):
        "has all marriage info, returns cleaned data"
        form = EnrolmentChecklistForm()
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
        form = EnrolmentChecklistForm()
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
        form = EnrolmentChecklistForm()
        form.cleaned_data = {
            'household_member': household_member,
            'initials': 'EE'}
        self.assertRaisesRegexp(ValidationError, 'Initials do not match', form.clean)
        self.assertRaisesRegexp(ValidationError, 'Martin', form.clean)

#     def test_updated_household_member(self):
#         plot = PlotFactory()
#         household_member = HouseholdMemberFactory(
#             household_structure=plot.household_structure,
#             first_name='Malcolm',
#             initials='MXE',
#             gender='M',
#             age_in_years=20,
#             present_today='Yes'
#             )
#         pk = household_member.pk
#         self.assertFalse(household_member.eligible_subject)
#         form = EnrolmentChecklistForm()
#         form.cleaned_data = {
#             'household_member': household_member,
#             'initials': 'MXE',
#             'citizen': 'Yes'}
#         household_member = HouseholdMember.objects.get(pk=pk)
#         self.assertTrue(household_member.eligible_subject)
