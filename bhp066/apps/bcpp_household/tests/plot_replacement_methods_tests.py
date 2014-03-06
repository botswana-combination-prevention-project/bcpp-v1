from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.test import TestCase

from edc.map.classes import site_mappers, Mapper
from edc.map.exceptions import MapperError

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_household.classes import ReplacementData
from apps.bcpp_household_member.models import SubjectAbsentee, SubjectAbsenteeEntry
from apps.bcpp_survey.tests.factories import SurveyFactory

from ..forms import PlotForm
from ..models import Household, HouseholdStructure, HouseholdLog, HouseholdLogEntry, Plot
from edc.map.classes import site_mappers

from .factories import PlotFactory

class PlotReplcamentMethodTests(TestCase):

    def setUp(self):
        SurveyFactory()

    def test_replace_refusal_plot(self):

        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status='occupied',
                eligible_members=3,
                report_datetime=datetime.date.today(),
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.6666599,
                gps_degrees_e=25,
                gps_minutes_e=44.466660,
                selected=2,
                access_attempts=0,)
        households = Household.objects.filter(plot=plot)
        house2 = households[1]
        house2.allowed_to_enumerate='yes'
        house2.save()
        h_structure = HouseholdStructure.objects.get(household=households[0])
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='MOSIMANE',
                initials='MB',
                gender='M',
                age_in_years=24,
                present_today='Yes',
                member_status='REFUSED')
        member.save()
        #refusal with one household
        self.assertEqual(ReplacementData.replace_refusals(plot), [households])

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='occupied',
                eligible_members=3,
                report_datetime=datetime.date.today(),
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5876399,
                gps_degrees_e=25,
                gps_minutes_e=44.8782599,
                selected=1,
                access_attempts=0,)
        household = Household.objects.filter(plot=plot)
        h_structure = HouseholdStructure.objects.get(household=household[0])
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='WANE',
                initials='WA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED')
        member.save()

        member = HouseholdMember(
                household_structure=h_structure,
                first_name='WANE',
                initials='WA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED')
        member.save()

        h_structure = HouseholdStructure.objects.get(household=household[1])
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='GOSIAME',
                initials='GS',
                gender='M',
                age_in_years=26,
                present_today='Yes',
                member_status='RESEARCH')
        member.save()
        member = HouseholdMember(household_structure=h_structure, first_name='THABANG',
                initials='TF', gender='F', age_in_years=27, present_today='Yes',
                member_status='RESEARCH')
        member.save()
        self.assertEqual(ReplacementData.replace_refusals(plot), [Household.objects.filter(plot=plot)])

    def test_replacement_absentees_ineligibles(self):
        print "*********************************"
        print "Absentee replacement"
        print "*****************************************"

        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status='occupied',
                eligible_members=3,
                report_datetime=datetime.date.today(),
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1,
                access_attempts=0,)
        household = Household.objects.filter(plot=plot)
        h_structure = HouseholdStructure.objects.get(household=household)
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='KGOSANA',
                initials='KB',
                gender='M',
                age_in_years=21,
                present_today='No',
                member_status='ABSENT')
        member.save()
        sub_absentee = SubjectAbsentee.objects.get(household_member=member)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        #refusal with one household
        self.assertEqual(ReplacementData.replacement_absentees_ineligibles(plot), [household])

        plot = PlotFactory(
                community='test_community',
                household_count=2,
                status='occupied',
                eligible_members=3,
                report_datetime=datetime.date.today(),
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
        h_structure = HouseholdStructure.objects.get(household=household[0])
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='KABELO',
                initials='KA',
                gender='M',
                age_in_years=29,
                present_today='Yes',
                member_status='ABSENT')
        member.save()
        sub_absentee = SubjectAbsentee.objects.get(household_member=member)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
        SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)

        member = HouseholdMember(
                household_structure=h_structure,
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

        h_structure = HouseholdStructure.objects.get(household=household[1])
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='BATHO',
                initials='BS',
                gender='M',
                age_in_years=26,
                present_today='Yes',
                member_status='RESEARCH')
        member.save()
        #A plot with more than one household
        self.assertEqual(ReplacementData.replacement_absentees_ineligibles(plot), [household[0]])

        def test_evaluate_head_of_household_refusal(self):
            plot = PlotFactory(
                community='test_community',
                household_count=1,
                status='occupied',
                eligible_members=3,
                report_datetime=datetime.date.today(),
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.88457999,
                gps_degrees_e=25,
                gps_minutes_e=44.9277000,
                selected=1,
                access_attempts=0,)
        households = Household.objects.filter(plot=plot)
        household = households[0]
        household.report_datetime = datetime.now()
        household.allowed_to_enumerate = 'No'
        household.save()

        self.assertEqual(ReplacementData.evaluate_head_of_household_refusal(household), household)
        
