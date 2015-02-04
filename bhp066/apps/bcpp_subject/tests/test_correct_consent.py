from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers, Mapper

from apps.bcpp_household.tests.factories import PlotFactory, HouseholdFactory, HouseholdStructureFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory, CorrectConsentFactory
from apps.bcpp_household_member.tests.factories import EnrollmentChecklistFactory
from apps.bcpp.app_configuration.classes import bcpp_app_configuration
from apps.bcpp_survey.models import Survey
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
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
    
    def startup(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        print "this is what i printed ***************", self.survey1.__dict__, "**************" 

    def test_las_tname(self):
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
        household = HouseholdFactory(plot=plot)
        household_structure = HouseholdStructureFactory(survey=self.survey1, household=household)
        household_member = HouseholdMemberFactory(household_structure=household_structure,last_name='BONNO', first_name='Bame', initials='BB')
        enrollment_checklist = EnrollmentChecklistFactory(household_member=household_member, initials='BB')
        subject_consent = SubjectConsentFactory(household_member=household_member, last_name='BONNO', first_name='Bame', initials='BB')
        correct_consent = CorrectConsentFactory(subject_consent=subject_consent, old_last_name='DIMO', new_last_name='DIMO')
        self.assertEquals(household_member.last_name, 'DINO')
        self.assertEquals(household_member.initials, 'BD')
        