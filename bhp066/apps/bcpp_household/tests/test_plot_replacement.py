from datetime import datetime, timedelta

from django.db import connections
from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.map.classes import Mapper
from edc.device.sync.utils import load_producer_db_settings, update_producer_from_settings
from edc.device.sync.tests.factories import ProducerFactory
from edc.device.dispatch.models.dispatch_item_register import DispatchItemRegister
from edc_constants.constants import NO
from bhp066.apps.bcpp.app_configuration.classes import bcpp_app_configuration
from bhp066.apps.bcpp_dispatch.classes import BcppDispatchController
from bhp066.apps.bcpp_household.constants import (
    ELIGIBLE_REPRESENTATIVE_PRESENT,
    ELIGIBLE_REPRESENTATIVE_ABSENT, NO_HOUSEHOLD_INFORMANT,
    NON_RESIDENTIAL, RESIDENTIAL_NOT_HABITABLE,
    RESIDENTIAL_HABITABLE, FIVE_PERCENT)
from bhp066.apps.bcpp_household.helpers import ReplacementHelper
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure, HouseholdLog
from bhp066.apps.bcpp_household_member.constants import REFUSED, ABSENT
from bhp066.apps.bcpp_household_member.models import HouseholdMember
from bhp066.apps.bcpp_household_member.models import SubjectAbsentee
from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp066.apps.bcpp_household_member.tests.factories import SubjectRefusalFactory, SubjectAbsenteeEntryFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey

from ..constants import (RARELY_NEVER_OCCUPIED, SEASONALLY_NEARLY_ALWAYS_OCCUPIED, UNKNOWN_OCCUPIED)
from .factories.plot_factory import PlotFactory
from .factories.household_log_entry_factory import HouseholdLogEntryFactory
from .factories.household_refusal_factory import HouseholdRefusalFactory
from .factories.household_assessment_factory import HouseholdAssessmentFactory
from .factories.reprentative_eligibility_factory import RepresentativeEligibilityFactory


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
            household_count=0,
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
        bcpp_dispatch.dispatch()
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_plots()), [(plot, dispatch_item_register)])
        self.teardown(producer.name)

    def test_replacement_plot2(self):
        """Assert helper returns an empty list if plot is not replaceable
        because it is just a plot in the 5 percent and is NON_RESIDENTIAL."""
        self.startup()
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
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
            bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
            bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.teardown(producer.name)

    def test_replacement_plot3(self):
        """Assert helper returns an empty list if plot is not replaceable
        replaces is not None even though RESIDENTIAL_HABITABLE."""
        self.startup()
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
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
            bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
            bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        self.assertEquals(list(replacement_helper.replaceable_plots(producer.name)), [])
        self.teardown(producer.name)

    def test_refusal_household1(self):
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household1, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household1, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household1, dispatch_item_register)])
        self.teardown(producer.name)

#     def test_absentees_ineligibles0(self):
#         """Asserts a household with 1 absent member and no other eligible members is replaceable"""
#         self.startup()
#         plot = PlotFactory(
#                 community='test_community',
#                 household_count=1,
#                 status=RESIDENTIAL_HABITABLE,
#                 eligible_members=3,
#                 description="A blue house with yellow screen wall",
#                 time_of_week='Weekdays',
#                 time_of_day='Morning',
#                 gps_degrees_s=25,
#                 gps_minutes_s=0.786540,
#                 gps_degrees_e=25,
#                 gps_minutes_e=44.8981199,
#                 selected=1)
#         household = Household.objects.get(plot=plot)
#         household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
#         RepresentativeEligibilityFactory(household_structure=household_structure)
#         self.household_member_absent_factory(
#             household_structure=household_structure,
#             gender='F',
#             age_in_years=51,
#             present_today='No',
#             study_resident='Yes')
#         member = HouseholdMember.objects.get(household_structure=household_structure)
#         member.member_status = BHS_SCREEN
#         member.save()
#         member = HouseholdMember.objects.get(household_structure=household_structure)
#         enrollment_checklist = EnrollmentChecklistFactory(
#                                 household_member=member,
#                                 initials='BB',
#                                 dob=date(1989, 10, 10),
#                                 gender='M',
#                                 guardian='N/A')
#         dob = date(date.today().year - member.age_in_years, 2, 1)
#         SubjectConsentFactory(household_member=member, dob=dob)
#         producer = ProducerFactory()
#         producer = update_producer_from_settings(producer)
#         # print producer.name
#         if not load_producer_db_settings():
#             raise TypeError('no producers')
#         self.create_survey_on_producer(producer.name)
#         bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
#         bcpp_dispatch.dispatch()
#         replacement_helper = ReplacementHelper()
#         options = dict(is_dispatched=True,
#                        item_app_label='bcpp_household',
#                        item_model_name='Plot',
#                        item_identifier=plot.pk)
#         dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
#         self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
#         self.teardown(producer.name)

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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        HouseholdAssessmentFactory(household_structure=household_structure,
                                   residency='No',
                                   last_seen_home=SEASONALLY_NEARLY_ALWAYS_OCCUPIED)  # Status value becomes seasonally occupied
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)
        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=RARELY_NEVER_OCCUPIED)  # Status value becomes rarely occupied
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
        HouseholdAssessmentFactory(household_structure=household_structure, residency='No', last_seen_home=RARELY_NEVER_OCCUPIED)  # Status value becomes never occupied
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
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
        HouseholdAssessmentFactory(household_structure=household_structure,
                                   residency=NO,
                                   last_seen_home=SEASONALLY_NEARLY_ALWAYS_OCCUPIED)
        producer = ProducerFactory()
        producer = update_producer_from_settings(producer)
        # print producer.name
        if not load_producer_db_settings():
            raise TypeError('no producers')
        self.create_survey_on_producer(producer.name)

        bcpp_dispatch = BcppDispatchController(using_source='default', using_destination=producer.name, dispatch_container_instance=plot)
        bcpp_dispatch.dispatch()
        replacement_helper = ReplacementHelper()
        options = dict(is_dispatched=True,
                       item_app_label='bcpp_household',
                       item_model_name='Plot',
                       item_identifier=plot.pk)
        dispatch_item_register = DispatchItemRegister.objects.using('default').get(**options)
        self.assertEquals(list(replacement_helper.replaceable_households(producer.name)), [(household, dispatch_item_register)])
        self.teardown(producer.name)

    def test_plot_replaces1(self):
        """Assert selects available plots correctly."""
        self.startup()
        PlotFactory(
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
        expected = [obj.plot_identifier for obj in [plot2, plot3, plot4, plot5]]
        expected.sort()
        # pprint.pprint(plot5.__dict__)
        self.assertEquals(available_plots, expected)
        self.teardown(producer.name)

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
        self.assertEqual(replacement_helper.plot, household_structure1.household.plot)
        self.assertEqual(replacement_helper.household, household_structure1.household)
        replacement_helper.household_structure = household_structure2
        self.assertRaises(TypeError, setattr(replacement_helper, 'plot', plot))
        self.assertEqual(replacement_helper.plot, household_structure2.household.plot)
        self.assertEqual(replacement_helper.household, household_structure2.household)
        self.teardown(producer.name)

    def test_household_replacement_reason1(self):
        """Assert replacement reason for refused members"""
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
        replacement_helper = ReplacementHelper()
        replacement_helper.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        reason = replacement_helper.household_replacement_reason
        self.assertEqual(reason, 'household all_eligible_members_refused')

    def test_household_replacement_reason2(self):
        """Asserts replacement reason for a household with a HOH who has refused."""
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
        replacement_helper = ReplacementHelper()
        replacement_helper.household_structure = HouseholdStructure.objects.get(household=household1, survey=self.survey1)
        reason = replacement_helper.household_replacement_reason
        self.assertEqual(reason, 'household refused_enumeration')

    def test_household_replacement_reason3(self):
        """Asserts a replacement reason for household with 3 enumeration attempts with no eligible representative present, that is replaceable"""
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
        replacement_helper = ReplacementHelper()
        replacement_helper.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        reason = replacement_helper.household_replacement_reason
        self.assertEqual(reason, 'household eligible_representative_absent')

    def test_household_replacement_reason4(self):
        """Asserts replacement reason for a household multiple members that are absent that its replaceable."""
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
        replacement_helper = ReplacementHelper()
        replacement_helper.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        reason = replacement_helper.household_replacement_reason
        self.assertEqual(reason, 'household all_eligible_members_absent')

    def test_household_replacement_reason5(self):
        """Asserts replacement reason for a household without an informant after 3 enumeration attempt is not replaceable if last_seen_home is unknown"""
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
        replacement_helper = ReplacementHelper()
        replacement_helper.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        reason = replacement_helper.household_replacement_reason
        self.assertEqual(reason, 'household failed_enumeration no_informant')
