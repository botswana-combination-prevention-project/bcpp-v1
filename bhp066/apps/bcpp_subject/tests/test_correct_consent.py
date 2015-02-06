from datetime import date

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers, Mapper

from apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, CorrectConsentFactory
from apps.bcpp_household_member.tests.factories import EnrollmentChecklistFactory
from apps.bcpp_household_member.models import EnrollmentChecklist, HouseholdMember
from apps.bcpp_subject.models import SubjectConsent
from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_survey.models import Survey
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_household.models import Household, HouseholdStructure
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory
from apps.bcpp_household.constants import (ELIGIBLE_REPRESENTATIVE_PRESENT,
                                           ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
                                           NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE,
                                           RESIDENTIAL_HABITABLE)


class TestCorrectConsent(TestCase):

    app_label = 'bcpp_subject'
    
    class TestPlotMapper(Mapper):
        map_area = 'test_community'
        map_code = '01'
        regions = []
        sections = []
        landmarks = []
        gps_center_lat = -25.033194
        gps_center_lon = 25.747139
        radius = 5.5
        location_boundary = ()
    # site_mappers.register(TestPlotMapper)
    
    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration 

    def test_lastname_and_initials(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey1, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent, 
                            old_last_name='BONNO', 
                            new_last_name='DIMO',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.initials, 'BD')
        self.assertEquals(enrollment_checklist.initials, 'BD')
        self.assertEquals(subject_consent.initials, 'BD')
        self.assertEquals(subject_consent.last_name, 'DIMO')

    def test_firstname_and_initials(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey1, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent, 
                            old_first_name='BAME', 
                            new_first_name='GAME',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.initials, 'GB')
        self.assertEquals(enrollment_checklist.initials, 'GB')
        self.assertEquals(subject_consent.initials, 'GB')
        self.assertEquals(household_member.first_name, 'GAME')
        self.assertEquals(subject_consent.first_name, 'GAME')

    def test_dob(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey1, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent, 
                            old_dob=date(1989, 10, 10), 
                            new_dob=date(1988, 1, 1),
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.age_in_years, 27)
        self.assertEquals(enrollment_checklist.dob, date(1988, 1, 1))
        self.assertEquals(subject_consent.dob, date(1988, 1, 1))

    def test_gender(self):
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(2)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(3)),)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(survey=self.survey1, household=household)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(
                            household_structure=household_structure, 
                            first_name='BAME', 
                            initials='BB', 
                            age_in_years=25,
                            gender='M')
        enrollment_checklist = EnrollmentChecklistFactory(
                                household_member=household_member, 
                                initials='BB', 
                                dob=date(1989, 10, 10),
                                gender='M',
                                guardian='N/A')
        
        subject_consent = SubjectConsentFactory(
                            household_member=household_member, 
                            last_name='BONNO', 
                            first_name='BAME', 
                            initials='BB', 
                            dob=date(1989, 10, 10),
                            gender='M',
                            may_store_samples='Yes',
                            is_literate='Yes')
        correct_consent = CorrectConsentFactory(
                            subject_consent=subject_consent, 
                            old_gender='M', 
                            new_gender='F',
                            )
        subject_consent = SubjectConsent.objects.get(household_member=household_member)
        household_member = subject_consent.household_member
        enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
        self.assertEquals(household_member.gender, 'F')
        self.assertEquals(enrollment_checklist.gender, 'F')
        self.assertEquals(subject_consent.gender, 'F')
