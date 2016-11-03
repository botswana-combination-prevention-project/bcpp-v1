from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.db.models import get_model
from django.test import TestCase

from edc_constants.constants import YES, NO, MALE
from edc.map.classes import site_mappers
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.registration.models import RegisteredSubject
from edc.core.bhp_variables.models import StudySite
from edc_constants.constants import NOT_APPLICABLE
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp066.apps.bcpp.app_configuration.classes import bcpp_app_configuration
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory


class TestClinicEligibilityForm(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'
    household_strucure = None
    subject_visit_female = None
    subject_visit_male = None
    household_member_female = None
    household_member_male = None
    data = {}

    def setUp(self):

        site_mappers.autodiscover()

        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

        self.household_structure = None
        self.registered_subject = None
        self.representative_eligibility = None
        self.study_site = None
        self.intervention = None

        self.community = site_mappers.get_current_mapper().map_area
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_current_mapper().map_code)
        self.site_code = self.study_site
        self.intervention = site_mappers.get_current_mapper().intervention
        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        self.survey2 = Survey.objects.get(survey_name='BCPP Year 2')  # see app_configuration
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.create_baseline(household)

        self.data = {
            'household_member': self.household_member_male.id,
            'report_datetime': datetime.today(),
            'first_name': 'SETS',
            'initials': 'SA',
            'dob': datetime.today() + relativedelta(years=-20),
            'guardian': NO,
            'gender': MALE,
            'has_identity': YES,
            'identity': '317918515',
            'identity_type': 'OMANG',
            'citizen': YES,
            'part_time_resident': YES,
            'literacy': YES,
            'guardian': YES,
            'inability_to_participate': 'N/A',
            'hiv_status': 'NEG',
            'legal_marriage': 'N/A',
            'marriage_certificate': 'N/A'
        }


    def create_baseline(self, household):
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        self.household_structure = household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)

        HouseholdMember = get_model('bcpp_household_member', 'HouseholdMember')

        self.household_member_female = HouseholdMember.objects.create(household_structure=household_structure,
                                                              first_name='SUE', initials='SW', gender='F',
                                                              age_in_years=25, study_resident='Yes', relation='sister',
                                                              inability_to_participate=NOT_APPLICABLE)
        self.household_member_male = HouseholdMember.objects.create(household_structure=household_structure,
                                                            first_name='ERIK', initials='EW', gender='M',
                                                            age_in_years=25, study_resident='Yes', relation='brother',
                                                            inability_to_participate=NOT_APPLICABLE)

    def test_validate_minor_not_valid(self):
        from bhp066.apps.bcpp_clinic.forms.clinic_eligibility_form import ClinicEligibilityForm
        clinic_form = ClinicEligibilityForm(data=self.data)
        self.assertIn(u"A minor age should be 16 or 17 years. Participart's age today 20 years.", clinic_form.errors.get("__all__"))
        self.assertFalse(clinic_form.is_valid())
        #print clinic_foddrm.errors

    def test_validate_minor_valid(self):
        from bhp066.apps.bcpp_clinic.forms.clinic_eligibility_form import ClinicEligibilityForm
        self.data['dob'] = datetime.today() + relativedelta(years=-16)
        clinic_form = ClinicEligibilityForm(data=self.data)
        self.assertTrue(clinic_form.is_valid())
