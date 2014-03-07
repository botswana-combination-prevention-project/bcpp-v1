import datetime

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
        print household
        household.allowed_to_enumerate='no'
        household.report_datetime = datetime.datetime.now()
        household.save()
        h_structure = HouseholdStructure.objects.get(household=household)
        member = HouseholdMember(
                household_structure=h_structure,
                first_name='MOSIMANE',
                initials='MB',
                gender='M',
                age_in_years=24,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')
        member.save()
        print ReplacementData().replace_refusals(plot),"its the 1 returning none"
        print household, "this is the househod to be returned"
        print h_structure, "STRUCTURE"
        print HouseholdMember.objects.filter(household_structure=h_structure), "Members"
        #refusal with one household
        print "**************************************************"
        print "Refusal with 1 household"
        self.assertEqual(ReplacementData().replace_refusals(plot), [household])
        print "**************************************************Done"

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
        household1=households[0]
        h_structure = HouseholdStructure.objects.get(household=household1)
        member1 = HouseholdMember(
                household_structure=h_structure,
                first_name='WANE',
                initials='WA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')
        member1.save()

        member2 = HouseholdMember(
                household_structure=h_structure,
                first_name='DANE',
                initials='DA',
                gender='M',
                age_in_years=25,
                present_today='Yes',
                member_status='REFUSED',
                study_resident='Yes')
        member2.save()

        household2=households[1]
        h_structure = HouseholdStructure.objects.get(household=household2)
        member3 = HouseholdMember(
                household_structure=h_structure,
                first_name='GOSIAME',
                initials='GS',
                gender='M',
                age_in_years=26,
                present_today='Yes',
                member_status='RESEARCH',
                study_resident='Yes')
        member3.save()
        member4 = HouseholdMember(household_structure=h_structure, first_name='THABANG',
                initials='TF', gender='F', age_in_years=27, present_today='Yes',
                member_status='RESEARCH')
        member4.save()
        
        print "*************************************************"
        print "refusal tests for 2 household 1 as a refusal"
        print "*************************************************"
        self.assertEqual(ReplacementData().replace_refusals(plot), [household1])
        print "*************************************************Done"

#     def test_replacement_absentees_ineligibles(self):
#         print "*********************************"
#         print "Absentee replacement"
#         print "*****************************************"
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
#         #refusal with one household
#         self.assertEqual(ReplacementData().replacement_absentees_ineligibles(plot), [household])

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
#         h_structure = HouseholdStructure.objects.get(household=household[0])
#         member = HouseholdMember(
#                 household_structure=h_structure,
#                 first_name='KABELO',
#                 initials='KA',
#                 gender='M',
#                 age_in_years=29,
#                 present_today='Yes',
#                 member_status='ABSENT')
#         member.save()
#         sub_absentee = SubjectAbsentee.objects.get(household_member=member)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
#         SubjectAbsenteeEntry.objects.filter(subject_absentee=sub_absentee)
# 
#         member = HouseholdMember(
#                 household_structure=h_structure,
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
#         h_structure = HouseholdStructure.objects.get(household=household[1])
#         member = HouseholdMember(
#                 household_structure=h_structure,
#                 first_name='BATHO',
#                 initials='BS',
#                 gender='M',
#                 age_in_years=26,
#                 present_today='Yes',
#                 member_status='RESEARCH')
#         member.save()
#         #A plot with more than one household
#         self.assertEqual(ReplacementData().replacement_absentees_ineligibles(plot), [household[0]])

    def test_evaluate_head_of_household_refusal(self):
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status='residential_habitable',
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.23117999,
            gps_degrees_e=25,
            gps_minutes_e=44.1667000,
            selected=1)
        households = Household.objects.filter(plot=plot)
        household = households[0]
        household.report_datetime = datetime.datetime.now()
        household.allowed_to_enumerate = 'no'
        household.save()
        
        print "*************************************************"
        print "Head of household refusal tests"
        print "*************************************************"
        print ReplacementData().evaluate_head_of_household_refusal(household), "Its here coli"
        self.assertEqual(ReplacementData().evaluate_head_of_household_refusal(household), household)

        print "*************************************************Done"