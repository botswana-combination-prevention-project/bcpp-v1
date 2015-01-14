# import pprint
import socket

from datetime import datetime, timedelta

from django.db import connections
from django.test import TestCase
from django.core.exceptions import ValidationError

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import site_mappers, Mapper
from edc.device.sync.utils import load_producer_db_settings, update_producer_from_settings
from edc.device.sync.tests.factories import ProducerFactory
from edc.device.sync.helpers import TransactionHelper

from apps.bcpp.app_configuration.classes import bcpp_app_configuration
from apps.bcpp_dispatch.classes import BcppDispatchController
from apps.bcpp_household.constants import (ELIGIBLE_REPRESENTATIVE_PRESENT,
                                           ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
                                           NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE,
                                           RESIDENTIAL_HABITABLE)
from apps.bcpp_household.helpers import ReplacementHelper
from apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLog, Plot
from apps.bcpp_household_member.constants import REFUSED, ABSENT
from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_household_member.models import SubjectAbsentee
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_household_member.tests.factories import SubjectRefusalFactory, SubjectAbsenteeEntryFactory
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_survey.models import Survey

from ..constants import NEARLY_ALWAYS_OCCUPIED, NEVER_OCCUPIED, SEASONALLY_OCCUPIED, RARELY_OCCUPIED, UNKNOWN_OCCUPIED, FIVE_PERCENT

from .factories import PlotFactory, HouseholdRefusalFactory, RepresentativeEligibilityFactory, HouseholdLogEntryFactory, HouseholdAssessmentFactory


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


class TestPlotReplacement(TestCase):

    def startup(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        bcpp_app_configuration.prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        self.dispatch_test_db = 'dispatch_destination'

    def teardown(self, producer_name):
        """Flushes the producer database."""
        cursor = connections[producer_name].cursor()
        cursor.execute("DELETE from bcpp_household_householdlogentry_audit")
        cursor.execute("DELETE from bcpp_household_householdlogentry")
        cursor.execute("DELETE from bcpp_household_householdlog_audit")
        cursor.execute("DELETE from bcpp_household_householdlog")
        cursor.execute("DELETE from bcpp_household_householdstructure_audit")
        cursor.execute("DELETE from bcpp_household_householdstructure")
        cursor.execute("DELETE from bcpp_household_household_audit")
        cursor.execute("DELETE from bcpp_household_household")
        cursor.execute("DELETE from bcpp_household_plot_audit")
        cursor.execute("DELETE from bcpp_household_plot")
        cursor.execute("DELETE from bhp_sync_outgoingtransaction")
        cursor.execute("DELETE from bhp_sync_incomingtransaction")

    def create_survey_on_producer(self, producer_name):
        try:
            Survey.objects.using(producer_name).get(
                survey_name=self.survey1.survey_name)
        except Survey.DoesNotExist:
            Survey.objects.using(producer_name).create(
                survey_name=self.survey1.survey_name,
                datetime_start=self.survey1.datetime_start,
                datetime_end=self.survey1.datetime_end)

    def household_member_refused_factory(self, **kwargs):
        household_member = HouseholdMemberFactory(**kwargs)
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = REFUSED
        household_member.save()
        household_member = HouseholdMember.objects.get(pk=pk)
        SubjectRefusalFactory(household_member=household_member)

    def household_member_absent_factory(self, **kwargs):
        household_member = HouseholdMemberFactory(**kwargs)
        pk = household_member.pk
        household_member = HouseholdMember.objects.get(pk=pk)
        household_member.member_status = ABSENT
        household_member.save()
        household_member = HouseholdMember.objects.get(pk=pk)
        subject_absentee = SubjectAbsentee.objects.get(household_member=household_member)
        SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee)
        SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee)
        SubjectAbsenteeEntryFactory(subject_absentee=subject_absentee)

    def test_replacement_plot1(self):
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=NON_RESIDENTIAL,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=FIVE_PERCENT,
            replaces='ERIK')
        replacement_helper = ReplacementHelper()
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default',
                                               using_destination=producer.name,
                                               dispatch_container_instance=plot)
#         bcpp_dispatch.dispatch()
        lis = replacement_helper.replaceable_plots()
        for l in list(lis):
            print l
        self.assertEquals(replacement_helper.replaceable_plots(), [plot])
        self.teardown(producer.name)

    def test_replacement_plot2(self):
        """Assert helper returns an empty list if plot is not replaceable
        because it is just a plot in the 5 percent and is NON_RESIDENTIAL."""
        self.startup()
        for i in range(0, 10):
            plot = PlotFactory(
                community='test_community',
                household_count=0,
                status=NON_RESIDENTIAL,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(i)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(i)),
                selected=FIVE_PERCENT,)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.teardown(producer.name)

    def test_replacement_plot3(self):
        """Assert helper returns an empty list if plot is not replaceable
        replaces is not None even though RESIDENTIAL_HABITABLE."""
        self.startup()
        for i in range(0, 10):
            plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.5666599 + float('0.000000{}'.format(i)),
                gps_degrees_e=25,
                gps_minutes_e=44.366660 + float('0.000000{}'.format(i)),
                selected=FIVE_PERCENT,
                replaces='H1234{}'.format(i))
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.teardown(producer.name)

    def test_refusal_household1(self):
        """Asserts that an enumerated household where ALL members refuse is replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=3,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        producer = ProducerFactory()
        update_producer_from_settings()
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        household, _, _ = Household.objects.filter(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        household_member = HouseholdMember(
            household_structure=household_structure,
            first_name='COOL',
            initials='CC',
            gender='M',
            member_status=REFUSED,
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        household_member.save()
        hm = HouseholdMember.objects.get(first_name='COOL')
        SubjectRefusalFactory(household_member=hm, reason='I don\'t have time', refusal_date=datetime.now())
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_refusal_household1a(self):
        """Asserts that a household of refused members is replaceable but if deleted is not replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=RESIDENTIAL_HABITABLE,
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
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_refusal_household2(self):
        """Asserts that a household of 3 refused members is replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=RESIDENTIAL_HABITABLE,
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
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=34,
            present_today='Yes',
            study_resident='Yes')
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=30,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_refusal_household3(self):
        """Asserts that a household of 3 refused members and two ineligible members is replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=RESIDENTIAL_HABITABLE,
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
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='M',
            age_in_years=34,
            present_today='Yes',
            study_resident='Yes')
        self.household_member_refused_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=30,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure,
            gender='F',
            age_in_years=70,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure,
            gender='F',
            age_in_years=12,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_refusal_household4(self):
        """Asserts that if 2 households in a plot, 1 household with 3 refused members, the household is replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=2,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        household2 = households[1]
        household_structure1 = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        household_structure2 = HouseholdStructure.objects.get(household=household2, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure1)
        RepresentativeEligibilityFactory(household_structure=household_structure2)
        self.household_member_refused_factory(
            household_structure=household_structure1,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        self.household_member_refused_factory(
            household_structure=household_structure1,
            gender='M',
            age_in_years=34,
            present_today='Yes',
            study_resident='Yes')
        self.household_member_refused_factory(
            household_structure=household_structure1,
            gender='F',
            age_in_years=30,
            present_today='Yes',
            study_resident='Yes')
        #hh2
        HouseholdMemberFactory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=70,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=12,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household1])
        self.teardown(producer.name)

    def test_refusal_household5(self):
        """Asserts that a household with 3 eligible members is not replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=2,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        households[1]
        household_structure1 = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure1)
        HouseholdMemberFactory(
            household_structure=household_structure1,
            gender='M',
            age_in_years=50,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure1,
            gender='M',
            age_in_years=34,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure1,
            gender='F',
            age_in_years=30,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_refusal_household6(self):
        """Asserts that a household with a HOH who has refused is replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=2,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        households = Household.objects.filter(plot=plot)
        household1 = households[0]
        households[1]
        household_structure = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        HouseholdRefusalFactory(household_structure=household_structure, report_datetime=datetime.now(), reason='not_interested')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household1])
        self.teardown(producer.name)

    def test_refusal_household7(self):
        """Asserts a plot with 2 households, A and B, where in household A the HOH has refused, A is replaceable."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=2,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.5666599,
            gps_degrees_e=25,
            gps_minutes_e=44.366660,
            selected=1)
        household1, household2 = Household.objects.filter(plot=plot)
        household_structure1 = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        household_structure2 = HouseholdStructure.objects.get(household=household2, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure1)
        RepresentativeEligibilityFactory(household_structure=household_structure2)
        HouseholdMemberFactory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=70,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=24,
            present_today='Yes',
            study_resident='Yes')
        HouseholdRefusalFactory(household_structure=household_structure1, report_datetime=datetime.now(), reason='not_interested')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household1])
        self.teardown(producer.name)

    def test_absentees_ineligibles1(self):
        """Asserts a household with 1 absent member and no other eligible members is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=51,
            present_today='No',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_absentees_ineligibles2(self):
        """Asserts a household multiple members that are absent that its replaceable."""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=51,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=34,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=23,
            present_today='No',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_absentees_ineligibles3(self):
        """Asserts a household 3 members absent and 2 not absent that is not replaceable."""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=51,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=34,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=23,
            present_today='No',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure,
            gender='F',
            age_in_years=70,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure,
            gender='F',
            age_in_years=24,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_check_absentees_ineligibles4(self):
        """Asserts a household initially is not replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles5(self):
        """Asserts a household without an informant after 3 enumeration attempt is replaceable if last_seen_home indicates 4_weeks_a_year"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=1))
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=SEASONALLY_OCCUPIED)  # Status value becomes seasonally occupied
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_absentees_ineligibles6(self):
        """Asserts a household without an informant after 3 enumeration attempt is replaceable if last_seen_home indicates 1_night_less_than_4_weeks_year"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=1))
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=RARELY_OCCUPIED)  # Status value becomes rarely occupied
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles7(self):
        """Asserts a household without an informant after 3 enumeration attempt is NOT replaceable if last_seen_home indicates never_spent_1_day_over_a_year"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=1))
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=NEVER_OCCUPIED)  # Status value becomes never occupied
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles8(self):
        """Asserts a household without an informant after 3 enumeration attempt is not replaceable if last_seen_home is unknown"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=1))
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=UNKNOWN_OCCUPIED)  # Status value becomes None
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_absentees_ineligibles9(self):
        """Asserts a household without an informant after 2 enumeration attempts is not replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles10(self):
        """Asserts a household without an informant after 1 enumeration attempt is not replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT,)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_check_absentees_ineligibles11(self):
        """Asserts a household with present member that is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_PRESENT,)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles12(self):
        """Asserts a household with 3 household log entries the last 1 with present status that is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_PRESENT, report_datetime=datetime.today() - timedelta(days=1))
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles13(self):
        """Asserts a household with 3 enumeration attempts with no eligible representative present, that is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=1))
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_absentees_ineligibles14(self):
        """Asserts a household with 1 enumeration attempts with no eligible representative present, that is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles15(self):
        """Asserts a household with 1 enumeration attempts with no eligible representative present, that is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=2))
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles16(self):
        """Asserts a household with 3 enumeration attempts with 2 no household informant and no eligible representative present that is replaceable"""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=1,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=1))
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_absentees_ineligibles17(self):
        """Asserts a household with 1 enumeration attempts with no eligible representative present, that is replaceable"""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT,)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [])
        self.teardown(producer.name)

    def test_absentees_ineligibles18(self):
        """Asserts a household without an informant after 3 enumeration
        attempt is replaceable if last_seen_home indicates 1_night_less_than_4_weeks_year"""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            selected=1)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        household_log = HouseholdLog.objects.get(household_structure=household_structure)
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log, household_status=NO_HOUSEHOLD_INFORMANT, report_datetime=datetime.today() - timedelta(days=1))
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=NEARLY_ALWAYS_OCCUPIED)  # Status value becomes nearly always occupied occupied
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.teardown(producer.name)

    def test_household_replacement1(self):
        """assert if an enumerated household with all members absent is replaced by a plot."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=1,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            selected=1)
        plot1 = PlotFactory(
            community='test_community',
            selected=FIVE_PERCENT)
        household = Household.objects.get(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure)
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=51,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=34,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure,
            gender='F',
            age_in_years=23,
            present_today='No',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default',
                                               using_destination=producer.name,
                                               dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        plot = Plot.objects.get(pk=plot.pk)
        household = Household.objects.get(pk=household.pk)
        self.assertEquals(household.plot.dispatched_to, producer.name)
        self.assertEquals(plot.dispatched_to, producer.name)
        TransactionHelper().outgoing_transactions(socket.gethostname(),
                                                  producer.name).delete()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [household])
        self.assertEquals(replacement_helper.replace_household(producer.name), [plot1])
        self.teardown(producer.name)

    def test_household_replacement2(self):
        """assert if a household is replaced by a plot."""
        self.startup()
        plot = PlotFactory(
                community='test_community',
                household_count=3,
                status=RESIDENTIAL_HABITABLE,
                eligible_members=3,
                description="A blue house with yellow screen wall",
                time_of_week='Weekdays',
                time_of_day='Morning',
                gps_degrees_s=25,
                gps_minutes_s=0.786540,
                gps_degrees_e=25,
                gps_minutes_e=44.8981199,
                selected=1)
        plot1 = PlotFactory(
                community='test_community',
                selected=FIVE_PERCENT)
        plot2 = PlotFactory(
                community='test_community',
                selected=FIVE_PERCENT)
        plot3 = PlotFactory(
                community='test_community',
                selected=FIVE_PERCENT)
        household1, household2, household3 = Household.objects.filter(plot=plot)
        household_structure1 = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        household_structure2 = HouseholdStructure.objects.get(household=household2, survey=self.survey1)
        household_structure3 = HouseholdStructure.objects.get(household=household3, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure1)
        RepresentativeEligibilityFactory(household_structure=household_structure2)
        RepresentativeEligibilityFactory(household_structure=household_structure3)
        self.household_member_absent_factory(
            household_structure=household_structure1,
            gender='F',
            age_in_years=51,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure1,
            gender='F',
            age_in_years=34,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure1,
            gender='F',
            age_in_years=23,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=24,
            present_today='No',
            study_resident='Yes')
        self.household_member_absent_factory(
            household_structure=household_structure3,
            gender='F',
            age_in_years=45,
            present_today='No',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)).sort(), ([household1, household2, household3]).sort())
        self.assertEquals(list(replacement_helper.replace_household(producer.name)).sort(), ([plot1, plot2, plot3]).sort())
        self.teardown(producer.name)

    def test_household_replacement3(self):
        """assert if a household is replaced by a plot."""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=2,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            selected=1)
        plot1 = PlotFactory(
            community='test_community',
            selected=FIVE_PERCENT)
        household1, household2 = Household.objects.filter(plot=plot)
        household_structure1 = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure1)
        household_structure2 = HouseholdStructure.objects.get(household=household2, survey=self.survey1)
        RepresentativeEligibilityFactory(household_structure=household_structure2)
        household_log1 = HouseholdLog.objects.get(household_structure=household_structure1)
        household_log2 = HouseholdLog.objects.get(household_structure=household_structure1)
        HouseholdLogEntryFactory(household_log=household_log2, household_status=ELIGIBLE_REPRESENTATIVE_PRESENT, report_datetime=datetime.today() - timedelta(days=4))
        HouseholdLogEntryFactory(household_log=household_log1, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=3))
        HouseholdLogEntryFactory(household_log=household_log1, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=2))
        HouseholdLogEntryFactory(household_log=household_log1, household_status=ELIGIBLE_REPRESENTATIVE_ABSENT, report_datetime=datetime.today() - timedelta(days=1))
        HouseholdMemberFactory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=70,
            present_today='Yes',
            study_resident='Yes')
        HouseholdMemberFactory(
            household_structure=household_structure2,
            gender='F',
            age_in_years=24,
            present_today='Yes',
            study_resident='Yes')
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        # replaceable_household = replacement_helper.replaceable_households(producer)
        self.assertEquals(replacement_helper.replaceable_households(producer), [household1])
        self.assertEquals(replacement_helper.replace_household(producer.name), [plot1])
        self.teardown(producer.name)

    def test_plot_replacement1(self):
        """Assert that a plot that is invalid with a plot status of non residential with another plot"""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            status=NON_RESIDENTIAL,
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces='H140993-02',
            selected=FIVE_PERCENT)
        plot1 = PlotFactory(
            community='test_community',
            selected=FIVE_PERCENT)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [plot])
        self.assertEquals(replacement_helper.replace_plot(producer.name), [plot1])
        self.teardown(producer.name)

    def test_plot_replacement2(self):
        """Assert that a plot that is invalid with a plot status of residential not habitable with another plot"""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_NOT_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces='H140993-02',
            replaced_by=None,
            htc=None,
            selected=FIVE_PERCENT)
        plot1 = PlotFactory(
            community='test_community',
            selected=FIVE_PERCENT)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot1)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [plot])
        self.assertEquals(replacement_helper.replace_plot(producer.name), [plot1])
        self.teardown(producer.name)

    def test_plot_replacement3(self):
        """Assert that a plot that is not invalid is not replaceable"""
        self.startup()
        plot = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces='H140993-02',
            replaced_by=None,
            htc=None,
            selected=FIVE_PERCENT)
        PlotFactory(community='test_community', selected=FIVE_PERCENT)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default',
                                               using_destination=producer.name,
                                               dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.assertEquals(replacement_helper.replace_plot(producer.name), [])
        self.teardown(producer.name)

    def test_plot_replaces1(self):
        """Assert selects available plots correctly."""
        self.startup()
        plot1 = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces='H140993-02',
            replaced_by=None,
            selected=FIVE_PERCENT)
        plot2 = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786542,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces=None,
            replaced_by=None,
            selected=FIVE_PERCENT)
        plot3 = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_NOT_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786543,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces=None,
            replaced_by=None,
            # htc=True,
            selected=FIVE_PERCENT)
        plot3.htc = True
        plot3.save(update_fields=['htc', 'replaced_by'])
        plot4 = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786544,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces=None,
            replaced_by=None,
            bhs=True,
            selected=FIVE_PERCENT)
        plot5 = PlotFactory(community='test_community', selected=FIVE_PERCENT)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        replacement_helper = ReplacementHelper()
        available_plots = [obj.plot_identifier for obj in replacement_helper.available_plots]
        available_plots.sort()
        expected = [obj.plot_identifier for obj in [plot2, plot5]]
        expected.sort()
        # pprint.pprint(plot5.__dict__)
        self.assertEquals(available_plots, expected)
        self.teardown(producer.name)

    def test_modify_plot(self):
        """Asserts that a plot cannot be modified if htc == True unless
        specified in update fields."""
        plot3 = PlotFactory(
            community='test_community',
            status=RESIDENTIAL_NOT_HABITABLE,
            gps_degrees_s=25,
            gps_minutes_s=0.786543,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            replaces=None,
            replaced_by=None,
            htc=None,
            bhs=None,
            selected=FIVE_PERCENT)
        plot3.htc = True
        self.assertRaises(ValidationError, plot3.save)
        try:
            plot3.save(update_fields=['htc'])
        except ValidationError:
            raise self.failureException('Did not expect ValidationError when changing plot.htc using update_fields.')

    def test_set_household_structure(self):
        self.startup()
        plot = PlotFactory(
            community='test_community',
            household_count=2,
            status=RESIDENTIAL_HABITABLE,
            eligible_members=3,
            description="A blue house with yellow screen wall",
            time_of_week='Weekdays',
            time_of_day='Morning',
            gps_degrees_s=25,
            gps_minutes_s=0.786540,
            gps_degrees_e=25,
            gps_minutes_e=44.8981199,
            selected=1)
        household1, household2 = Household.objects.filter(plot=plot)
        household_structure1 = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        household_structure2 = HouseholdStructure.objects.get(household=household2, survey=self.survey1)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        replacement_helper = ReplacementHelper(household_structure=household_structure1)
        replacement_helper.household_structure = household_structure2
        self.assertEqual(replacement_helper.plot, household_structure1.plot)
        self.assertEqual(replacement_helper.household, household_structure1.household)
        self.assertRaises(TypeError, setattr(replacement_helper, 'plot', plot))
        self.assertEqual(replacement_helper.plot, household_structure2.plot)
        self.assertEqual(replacement_helper.household, household_structure2.household)
        self.teardown(producer.name)
