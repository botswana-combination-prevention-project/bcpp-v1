import datetime

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers, Mapper

from apps.bcpp_household.classes import ReplacementData
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
from apps.bcpp_household_member.constants import REFUSED
from apps.bcpp_household_member.tests.factories import SubjectRefusalFactory
from apps.bcpp_survey.models import Survey
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, HouseholdRefusal, HouseholdAssessment

from .factories import HouseholdFactory
from .factories import PlotFactory


class TestPlotMapper(Mapper):
    map_area = 'test_community11'
    map_code = '094'
    regions = []
    sections = []
    landmarks = []
    gps_center_lat = -25.033194
    gps_center_lon = 25.747139
    radius = 5.5
    location_boundary = ()
site_mappers.register(TestPlotMapper)


class PlotReplcamentMethodTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration

    def household_member_refused_factory(self, **kwargs):
        household_member = HouseholdMemberFactory(**kwargs)
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = REFUSED
        household_member.save()
        household_member = HouseholdMember.objects.get(pk=pk)
        SubjectRefusalFactory(household_member=household_member)

    def test_check_refusal_household1(self):
        """Asserts that a household of refused members is replaceble."""

        plot = PlotFactory(
            community='test_community11',
            household_count=1,
            status='residential_habitable',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        self.assertEqual(ReplacementData().check_refusals(plot), [[household, 'all members refused', None]])

    def test_check_refusal_household2(self):
        """Asserts that a household of 3 refused members is replaceble."""

        plot = PlotFactory(
            community='test_community11',
            household_count=1,
            status='residential_habitable',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=34,
            present_today='Yes',
            study_resident='Yes')
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=30,
            present_today='Yes',
            study_resident='Yes')
        self.assertEqual(ReplacementData().check_refusals(plot), [[household, 'all members refused', None]])

    def test_check_refusal_household3(self):
        """Asserts that a household of 3 refused members is replaceble."""

        plot = PlotFactory(
            community='test_community11',
            household_count=1,
            status='residential_habitable',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=34,
            present_today='Yes',
            study_resident='Yes')
        household_member = self.household_member_refused_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=30,
            present_today='Yes',
            study_resident='Yes')
        household_member = HouseholdMemberFactory(
            household_structure=household_structure,
            gender='F',
            age_in_years=70,
            present_today='Yes',
            study_resident='Yes')
        household_member = HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender='F',
            age_in_years=12,
            present_today='Yes',
            study_resident='Yes')
        self.assertEqual(ReplacementData().check_refusals(plot), [[household, 'all members refused', None]])

#     def test_check_refusal_household5(self):
#         """Check for refusals for a plot with more than one household."""
#  
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=2,
#                 status='residential_habitable',
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.7876399,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.8782599,
#                 selected=1)
#         households = Household.objects.filter(plot=plot)
#         household1 = households[0]
#         household_structure = HouseholdStructure.objects.filter(household=household1).order_by('created')
#         household_log = HouseholdLog(household_structure=household_structure[0])
#         household_log.save()
#         household_log_entry1 = HouseholdLogEntry(household_log=household_log, household_status='eligible_representative_present', report_datetime=datetime.datetime.now())
#         household_log_entry1.save()
#         member1 = HouseholdMember(
#                 household_structure=household_structure[0],
#                 first_name='WANE',
#                 initials='WA',
#                 gender='M',
#                 age_in_years=25,
#                 present_today='Yes',
#                 member_status='REFUSED',
#                 study_resident='Yes')
#         member1.save()
#  
#         member2 = HouseholdMember(
#                 household_structure=household_structure[0],
#                 first_name='DANE',
#                 initials='DA',
#                 gender='M',
#                 age_in_years=25,
#                 present_today='Yes',
#                 member_status='REFUSED',
#                 study_resident='Yes')
#         member2.save()
#  
#         household2 = households[1]
#         household_structure = HouseholdStructure.objects.filter(household=household2).order_by('created')
#         member3 = HouseholdMember(
#                 household_structure=household_structure[0],
#                 first_name='GOSIAME',
#                 initials='GS',
#                 gender='M',
#                 age_in_years=26,
#                 present_today='Yes',
#                 member_status='RESEARCH',
#                 study_resident='Yes')
#         member3.save()
#         member4 = HouseholdMember(household_structure=household_structure[0], first_name='THABANG',
#                 initials='TF', gender='F', age_in_years=27, present_today='Yes',
#                 member_status='RESEARCH')
#         member4.save()
#  
#         self.assertEqual(ReplacementData().check_refusals(plot), [[household1, 'all members refused', None]])
 
#     def test_check_refusal_household3(self):
#         """Test for household refusal by head of household."""
# 
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=2,
#                 status='residential_habitable',
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.7276399,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.2782599,
#                 selected=1)
#         households = Household.objects.filter(plot=plot)
#         household1 = households[0]
#         household_structure = HouseholdStructure.objects.get(household=household1)
#         household_log = HouseholdLog(household_structure=household_structure)
#         household_log.save()
#         household_log_entry = HouseholdLogEntry(household_log=household_log, household_status='refused', report_datetime=datetime.datetime.now())
#         household_log_entry.save()
#         household_refusal = HouseholdRefusal(household=household1, report_datetime=datetime.datetime.now(), reason='not_interested')
#         household_refusal.save()
# 
#         self.assertEqual(ReplacementData().check_refusals(plot), [household1, 'HOH refusal'])
# 
#     def test_check_absentees_ineligibles1(self):
#         """""Test for absentees for a plot with one household"""
# 
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=1,
#                 status='residential_habitable',
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.786540,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.8981199,
#                 selected=1)
#         household = Household.objects.filter(plot=plot)
#         h_structure = HouseholdStructure.objects.get(household=household)
#         member = HouseholdMember(
#                 household_structure=h_structure,
#                 first_name='KGOSANA',
#                 initials='KB',
#                 gender='M',
#                 age_in_years=21,
#                 present_today='No',
#                 member_status='ABSENT')
#         member.save()
#         sub_absentee = SubjectAbsentee.objects.get(household_member=member)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
# 
#         self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household, 'all members are absent'])
# 
#     def test_check_absentees_ineligibles2(self):
#         """Test for abseentees for a plot with more than one household."""
# 
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=2,
#                 status='residential_habitable',
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.88457999,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.9277000,
#                 selected=1,
#                 access_attempts=0,)
#         household = Household.objects.filter(plot=plot)
#         household_structure = HouseholdStructure.objects.get(household=household[0])
#         member = HouseholdMember.objects.create(
#                 household_structure=household_structure,
#                 first_name='KABELO',
#                 initials='KA',
#                 gender='M',
#                 age_in_years=29,
#                 present_today='Yes',
#                 member_status='ABSENT')
#         sub_absentee = SubjectAbsentee.objects.get(household_member=member)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
# 
#         member = HouseholdMember(
#                 household_structure=household_structure,
#                 first_name='DILO',
#                 initials='DA',
#                 gender='M',
#                 age_in_years=25,
#                 present_today='Yes',
#                 member_status='ABSENT')
#         member.save()
#         sub_absentee = SubjectAbsentee.objects.get(household_member=member)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
# 
#         household_structure = HouseholdStructure.objects.get(household=household[1])
#         member = HouseholdMember(
#                 household_structure=household_structure,
#                 first_name='BATHO',
#                 initials='BS',
#                 gender='M',
#                 age_in_years=26,
#                 present_today='Yes',
#                 member_status='RESEARCH')
#         member.save()
# 
#         self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household[0], 'all members are absent'])
# 
#     def test_check_absentees_ineligibles3(self):
#         """Test for no informant within a household, an absent household that members are seasonally around."""
# 
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=2,
#                 status='residential_habitable',
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.51276399,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.311,
#                 selected=1)
#         households = Household.objects.filter(plot=plot)
#         household1 = households[0]
#         household_structure = HouseholdStructure.objects.get(household=household1)
#         household_log = HouseholdLog(household_structure=household_structure)
#         household_log.save()
#         household_log_entry1 = HouseholdLogEntry(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now())
#         household_log_entry1.save()
#         household_log_entry2 = HouseholdLogEntry(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
#         household_log_entry2.save()
#         household_log_entry3 = HouseholdLogEntry(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
#         household_log_entry3.save()
#         household_assessment = HouseholdAssessment(household=household1, residency='No', last_seen_home='1_to_6_months', most_likely=['work_live_school_outside_village', 'away_for_harvesting'])
#         household_assessment.save()
# 
#         self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household1, 'no household informant'])
# 
#     def test_check_absentees_ineligibles4(self):
#         """Test for no informant within a household, an absent household with members that are rarely there."""
# 
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=2,
#                 status='residential_habitable',
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.593,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.999,
#                 selected=1)
#         households = Household.objects.filter(plot=plot)
#         household1 = households[0]
#         household_structure = HouseholdStructure.objects.get(household=household1)
#         household_log = HouseholdLog(household_structure=household_structure)
#         household_log.save()
#         household_log_entry1 = HouseholdLogEntry(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now())
#         household_log_entry1.save()
#         household_log_entry2 = HouseholdLogEntry(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
#         household_log_entry2()
#         household_log_entry3 = HouseholdLogEntry(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
#         household_log_entry3.save()
#         household_assessment = HouseholdAssessment.objects.create(household=household1, residency='No', last_seen_home='1_to_6_months', most_likely=['work_live_school_outside_village', 'away_for_harvesting'])
#         household_assessment.save()
# 
#         self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household1, 'no household informant'])
# 
#     def test_is_hoh_refused(self):
#         """Test for a head of household refusal."""
# 
#         household = HouseholdFactory()
#         household_structure = HouseholdStructure.objects.get(household=household)
#         household_log = HouseholdLog(household_structure=household_structure)
#         household_log.save()
#         household_log_entry1 = HouseholdLogEntry(household_log=household_log, household_status='refused', report_datetime=datetime.datetime.now())
#         household_log_entry1.save()
#         household_refusal = HouseholdRefusal(household=household, report_datetime=datetime.datetime.now(), reason='not_interested')
#         household_refusal.save()
# 
#         self.assertEqual(ReplacementData().is_hoh_refused(household), household)
# 
#     def test_is_refusal(self):
#         """Test for household memebers reefusing."""
# 
#         household = HouseholdFactory()
#         household_structure = HouseholdStructure.objects.get(household=household)
#         household_log = HouseholdLog(household_structure=household_structure)
#         household_log.save()
#         household_log_entry1 = HouseholdLogEntry(household_log=household_log, household_status='eligible_representative_present', report_datetime=datetime.datetime.now())
#         household_log_entry1.save()
#         member1 = HouseholdMember(
#                 household_structure=household_structure,
#                 first_name='KIM',
#                 initials='KK',
#                 gender='M',
#                 age_in_years=25,
#                 present_today='Yes',
#                 member_status='REFUSED',
#                 study_resident='Yes')
#         member1.save()
# 
#         member2 = HouseholdMember(
#                 household_structure=household_structure,
#                 first_name='PAUL',
#                 initials='PR',
#                 gender='M',
#                 age_in_years=25,
#                 present_today='Yes',
#                 member_status='REFUSED',
#                 study_resident='Yes')
#         member2.save()
#         self.assertEqual(ReplacementData().is_refusal(household), household)
