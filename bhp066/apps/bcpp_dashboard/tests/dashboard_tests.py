from dateutil.relativedelta import relativedelta
from datetime import datetime

from django.test import TestCase

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.map.classes import site_mappers
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.testing.classes import TestVisitSchedule
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestScheduledModel1Factory, TestRequisitionFactory

from apps.bcpp_household.models import HouseholdStructure, Household
from apps.bcpp_household.tests.factories import HouseholdFactory, PlotFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_subject.tests.factories import SubjectConsentFactory
from apps.bcpp_subject.tests import BaseScheduledModelTestCase
from apps.bcpp_survey.tests.factories import SurveyFactory

from ..classes import HouseholdDashboard, SubjectDashboard


class DashboardTests(TestCase):

    app_label = 'testing'

    def setUp(self):
        from edc.testing.tests.factories import TestVisitFactory
        self.test_visit_factory = TestVisitFactory
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(content_type__model='TestConsentWithMixin'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)

        test_visit_schedule = TestVisitSchedule()
        test_visit_schedule.rebuild()

        self.visit_definition = VisitDefinition.objects.get(code='1000')

        self.test_consent = TestConsentWithMixinFactory(gender='M')

        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject)

        self.survey1 = SurveyFactory(
            datetime_start=datetime.today() + relativedelta(months=-5),
            datetime_end=datetime.today() + relativedelta(days=5))
        self.survey2 = SurveyFactory(
            datetime_start=datetime.today() + relativedelta(months=-5, years=1),
            datetime_end=datetime.today() + relativedelta(months=5, years=1))
        self.survey3 = SurveyFactory(
            datetime_start=datetime.today() + relativedelta(months=-5, years=2),
            datetime_end=datetime.today() + relativedelta(months=5, years=2))

        site_mappers.autodiscover()

        mapper = site_mappers.get(site_mappers.get_as_list()[0])

        self.community = mapper().get_map_area()

        self.plot = PlotFactory(community=self.community)
        self.plot.gps_degrees_s, self.plot.gps_minutes_s, self.plot.gps_degrees_e, self.plot.gps_minutes_e = mapper().test_location
        self.plot.household_count = 2
        self.plot.status = 'occupied'
        self.plot.save()

        self.household1 = Household.objects.filter(plot=self.plot).order_by('created')[0]
        self.household_structure1 = HouseholdStructure.objects.get(household=self.household1, survey=self.survey1)
        self.household2 = Household.objects.filter(plot=self.plot).order_by('created')[1]
        self.household_member1 = HouseholdMemberFactory(household_structure=self.household_structure1,
                                                        age_in_years=26,
                                                        present_today='Yes',
                                                        member_status='RESEARCH')
        self.household_member2 = HouseholdMemberFactory(household_structure=self.household_structure1, age_in_years=36, present_today='Yes')
        self.household_member3 = HouseholdMemberFactory(household_structure=self.household_structure1, age_in_years=12, present_today='Yes')
        self.household_member4 = HouseholdMemberFactory(household_structure=self.household_structure1, age_in_years=99, present_today='Yes')
        self.dashboard_type = 'household'
        self.dashboard_model = 'household'
        self.dashboard_id = self.household1.pk

        self.household_member1.eligible_subject = True

        self.subject_consent = SubjectConsentFactory(
            household_member=self.household_member1,
            first_name=self.household_member1.first_name,
            initials=self.household_member1.initials,
            registered_subject=self.household_member1.registered_subject)

    def test_create_household_dashboard1(self):
        dashboard_type = 'household'
        dashboard_model = 'household'
        dashboard_id = self.household1.pk
        household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model)
        household_dashboard.set_context()

    def test_create_household_dashboard2(self):
        dashboard_type = 'household_structure'
        dashboard_model = 'household_structure'
        dashboard_id = self.household_structure1.pk
        household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model)
        household_dashboard.set_context()
