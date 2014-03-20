import datetime

from django.test import TestCase

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household.classes import ReplacementData
from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
from apps.bcpp_survey.tests.factories import SurveyFactory

from ..models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, HouseholdRefusal, HouseholdAssessment

from .factories import PlotFactory, HouseholdFactory


class PlotReplcamentMethodTests(TestCase):

    def setUp(self):
        SurveyFactory()

    def test_check_refusal_household1(self):
        """Check for a refusal for a plot with one household."""

        plot = PlotFactory(
                community='test_community',
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
        household_structure = HouseholdStructure.objects.get(household=household)
        member = HouseholdMember(
                household_structure=household_structure,
                first_name='MOSIMANE',
                initials='MB',
                gender='M',
                age_in_years=24,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')
        member.save()
        self.assertEqual(ReplacementData().check_refusals(plot), [household, 'all members refused'])

    def test_check_refusal_household2(self):
        """Check for refusals for a plot with more than one household."""

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='residential_habitable',
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.7876399,
                gps_degrees_e=25,
                gps_minutes_e=44.8782599,
                selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        household_structure = HouseholdStructure.objects.get(household=household1)
        household_log = HouseholdLog.objects.create(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='eligible_representative_present', report_datetime=datetime.datetime.now())
        member1 = HouseholdMember.objects.create(
                household_structure=household_structure,
                first_name='WANE',
                initials='WA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')

        member2 = HouseholdMember.objects.create(
                household_structure=household_structure,
                first_name='DANE',
                initials='DA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')

        household2 = households[1]
        household_structure = HouseholdStructure.objects.get(household=household2)
        member3 = HouseholdMember(
                household_structure=household_structure,
                first_name='GOSIAME',
                initials='GS',
                gender='M',
                age_in_years=26,
                present_today='Yes',
                member_status='RESEARCH',
                study_resident='Yes')
        member3.save()
        member4 = HouseholdMember(household_structure=household_structure, first_name='THABANG',
                initials='TF', gender='F', age_in_years=27, present_today='Yes',
                member_status='RESEARCH')
        member4.save()

        self.assertEqual(ReplacementData().check_refusals(plot), [household1, 'all members refused'])

    def test_check_refusal_household3(self):
        """Test for household refusal by head of household."""

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='residential_habitable',
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.7276399,
                gps_degrees_e=25,
                gps_minutes_e=44.2782599,
                selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        household_structure = HouseholdStructure.objects.get(household=household1)
        household_log = HouseholdLog.objects.create(household_structure=household_structure)
        household_log_entry = HouseholdLogEntry.objects.create(household_log=household_log, household_status='refused', report_datetime=datetime.datetime.now())
        household_refusal = HouseholdRefusal.objects.create(household=household1, report_datetime=datetime.datetime.now(), reason='not_interested')

        self.assertEqual(ReplacementData().check_refusals(plot), [household1, 'HOH refusal'])

    def test_check_absentees_ineligibles1(self):
        """""Test for absentees for a plot with one household"""

        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status='residential_habitable',
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.filter(plot=plot)
        h_structure = HouseholdStructure.objects.get(household=household)
        member = HouseholdMember.objects.create(
                household_structure=h_structure,
                first_name='KGOSANA',
                initials='KB',
                gender='M',
                age_in_years=21,
                present_today='No',
                member_status='ABSENT')
        sub_absentee = SubjectAbsentee.objects.get(household_member=member)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)

        self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household, 'all members are absent'])

    def test_check_absentees_ineligibles2(self):
        """Test for abseentees for a plot with more than one household."""

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='residential_habitable',
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.88457999,
                gps_degrees_e=25,
                gps_minutes_e=44.9277000,
                selected=1,
                access_attempts=0,)
        household = Household.objects.filter(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household[0])
        member = HouseholdMember.objects.create(
                household_structure=household_structure,
                first_name='KABELO',
                initials='KA',
                gender='M',
                age_in_years=29,
                present_today='Yes',
                member_status='ABSENT')
        sub_absentee = SubjectAbsentee.objects.get(household_member=member)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)

        member = HouseholdMember(
                household_structure=household_structure,
                first_name='DILO',
                initials='DA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='ABSENT')
        member.save()
        sub_absentee = SubjectAbsentee.objects.get(household_member=member)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)

        household_structure = HouseholdStructure.objects.get(household=household[1])
        member = HouseholdMember.objects.create(
                household_structure=household_structure,
                first_name='BATHO',
                initials='BS',
                gender='M',
                age_in_years=26,
                present_today='Yes',
                member_status='RESEARCH')

        self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household[0], 'all members are absent'])

    def test_check_absentees_ineligibles3(self):
        """Test for no informant within a household, an absent household that members are seasonally around."""

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='residential_habitable',
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.51276399,
                gps_degrees_e=25,
                gps_minutes_e=44.311,
                selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        household_structure = HouseholdStructure.objects.get(household=household1)
        household_log = HouseholdLog.objects.create(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now())
        household_log_entry2 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
        household_log_entry3 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
        household_assessment = HouseholdAssessment.objects.create(household=household1, residency='No', last_seen_home='1_to_6_months', most_likely=['work_live_school_outside_village', 'away_for_harvesting'])

        self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household1, 'no household informant'])

    def test_check_absentees_ineligibles4(self):
        """Test for no informant within a household, an absent household with members that are rarely there."""

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='residential_habitable',
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.593,
                gps_degrees_e=25,
                gps_minutes_e=44.999,
                selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        household_structure = HouseholdStructure.objects.get(household=household1)
        household_log = HouseholdLog.objects.create(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now())
        household_log_entry2 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
        household_log_entry3 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='no_household_informant', report_datetime=datetime.datetime.now() + datetime.timedelta(days=1))
        household_assessment = HouseholdAssessment.objects.create(household=household1, residency='No', last_seen_home='1_to_6_months', most_likely=['work_live_school_outside_village', 'away_for_harvesting'])

        self.assertEqual(ReplacementData().check_absentees_ineligibles(plot), [household1, 'no household informant'])

    def test_is_hoh_refused(self):
        """Test for a head of household refusal."""

        household = HouseholdFactory()
        household_structure = HouseholdStructure.objects.get(household=household)
        household_log = HouseholdLog.objects.create(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='refused', report_datetime=datetime.datetime.now())
        household_refusal = HouseholdRefusal.objects.create(household=household, report_datetime=datetime.datetime.now(), reason='not_interested')

        self.assertEqual(ReplacementData().is_hoh_refused(household), household)

    def test_is_refusal(self):
        """Test for household memebers reefusing."""

        household = HouseholdFactory()
        household_structure = HouseholdStructure.objects.get(household=household)
        household_log = HouseholdLog.objects.create(household_structure=household_structure)
        household_log_entry1 = HouseholdLogEntry.objects.create(household_log=household_log, household_status='eligible_representative_present', report_datetime=datetime.datetime.now())
        member1 = HouseholdMember.objects.create(
                household_structure=household_structure,
                first_name='KIM',
                initials='KK',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')

        member2 = HouseholdMember.objects.create(
                household_structure=household_structure,
                first_name='PAUL',
                initials='PR',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')
        self.assertEqual(ReplacementData().is_refusal(household), household)
