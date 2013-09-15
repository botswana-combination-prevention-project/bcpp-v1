import re
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.test import TestCase
from django.db import IntegrityError
from bcpp_dashboard.classes import SubjectDashboard, HtcSubjectDashboard
from django.contrib.contenttypes.models import ContentType
from bhp_content_type_map.models import ContentTypeMap
# from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_lab_tracker.classes import site_lab_tracker
from bhp_map.classes import site_mappers
from bhp_visit.tests.factories import VisitDefinitionFactory, ScheduleGroupFactory, MembershipFormFactory
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_appointment.models import Configuration
from bhp_consent.tests.factories import ConsentCatalogueFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_household.models import HouseholdStructure
from bcpp_household.tests.factories import HouseholdFactory, PlotFactory
# from bcpp_subject.tests.factories import SubjectConsentFactory
from bcpp_htc_subject.tests.factories import HtcSubjectConsentFactory
from bcpp_survey.tests.factories import SurveyFactory


class DashboardTests(TestCase):

    def test_p1(self):
        site_lab_tracker.autodiscover()
        site_mappers.autodiscover()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
#         content_type = ContentType.objects.get(app_label='bcpp_household', model='maternalenrollment')
#         content_type_map = ContentTypeMap.objects.get(content_type=content_type)
#         membership_form = MembershipFormFactory(content_type_map=content_type_map, category='maternal')
#         schedule_group = ScheduleGroupFactory(membership_form=membership_form)
#         visit_tracking_content_type_map = ContentTypeMap.objects.get(app_label='maikalelo_maternal', model='maternalvisit')
#         visit_definition = VisitDefinitionFactory(visit_tracking_content_type_map=visit_tracking_content_type_map)
#         visit_definition.schedule_group.add(schedule_group)

        Configuration.objects.create()
#         print 'get a community name from the mapper classes'
#         community = site_mappers.get_as_list()[0]
#         print 'create a new survey'
#         survey1 = SurveyFactory(datetime_start=datetime(2013, 07, 01), datetime_end=datetime(2013,12,01))
#         survey2 = SurveyFactory(datetime_start=datetime(2014, 01, 01), datetime_end=datetime(2014,07,01))
#         survey3 = SurveyFactory(datetime_start=datetime(2015, 01, 01), datetime_end=datetime(2015,07,01))
#         print 'create a new Plot in community {0}.'.format(community)
#         plot = PlotFactory(community=community)
#         household = HouseholdFactory(plot=plot)
#         print household.community
#         dashboard_type = 'household'
#         dashboard_model = 'household'
#         dashboard_id = household.pk
#         print 'initialize the HH dashboard'
#         household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model)

        self.setup_dashboard(self)

        print 'assert household structure exists for this HH and the three surveys'
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)
        household_structure = self.household_dashboard.get_household_structure()
        print 'create another new HH in community {0}.'.format(self.community)
        HouseholdFactory(plot=self.plot)
        print 'assert no hh structure created'
        self.assertEquals(HouseholdStructure.objects.all().count(), 6)  # 2 surveys for each HH = 2 x 3 = 6
        print 'create HH members for this survey and HH {0}'.format(self.household)
        hm1 = HouseholdMemberFactory(household_structure=household_structure)
        print hm1.registered_subject.pk
        hm2 = HouseholdMemberFactory(household_structure=household_structure)
        print hm2.registered_subject.pk
        hm3 = HouseholdMemberFactory(household_structure=household_structure)
        print hm3.registered_subject.pk
        hm4 = HouseholdMemberFactory(household_structure=household_structure)
        print hm4.registered_subject.pk

        print 'fail on attempt to create consent using household member with different first name and initials than household member'
        self.assertRaises(IntegrityError, HtcSubjectConsentFactory, household_member=hm1)
        print 'consent {0}'.format(hm1)
        HtcSubjectConsentFactory(household_member=hm1, first_name=hm1.first_name, initials=hm1.initials, registered_subject=hm1.registered_subject)
        content_type = ContentType.objects.get(app_label='bcpp_subject', model='subjectconsent')
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        ConsentCatalogueFactory(content_type_map=content_type_map, add_for_app='bcpp_subject')

        dashboard_type = 'subject'
        dashboard_model = 'household_member'
        household_member = HouseholdMemberFactory()
        dashboard_id = household_member.pk
        SubjectDashboard(
            dashboard_type=dashboard_type,
            dashboard_model=dashboard_model,
            dashboard_id=dashboard_id,
            )

        HtcSubjectConsentFactory()
        content_type = ContentType.objects.get(app_label='bcpp_subject', model='htcsubjectconsent')
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        ConsentCatalogueFactory(content_type_map=content_type_map, add_for_app='bcpp_subject_htc')

        content_type = ContentType.objects.get(app_label='bcpp_subject_htc', model='htcregistration')
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        membership_form = MembershipFormFactory(content_type_map=content_type_map, category='htc_subject')
        schedule_group = ScheduleGroupFactory(membership_form=membership_form)
        visit_tracking_content_type_map = ContentTypeMap.objects.get(app_label='bcpp_subject_htc', model='htcsubjectvisit')
        visit_definition = VisitDefinitionFactory(visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        dashboard_type = 'infant'
        dashboard_model = 'birth'
        household_member = HouseholdMemberFactory()
        dashboard_id = household_member.pk
        HtcSubjectDashboard(
            dashboard_type=dashboard_type,
            dashboard_model=dashboard_model,
            dashboard_id=dashboard_id,
            )


def setup_dashboard(inst):

    inst.re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
    inst.survey1 = None
    inst.survey2 = None
    inst.survey3 = None
    inst.survey4 = None
    inst.plot = None
    inst.household = None
    inst.household2 = None
    inst.household_structure = None
    inst.household_member1 = None
    inst.household_member2 = None
    inst.household_member3 = None
    inst.household_member4 = None
    inst.dashboard_type = None
    inst.dashboard_id = None
    inst.dashboard_model = None
    inst.community = None
    inst.household_dashboard = None
    print 'create survey, plot, household, and household_member'
    print 'create three surveys where NONE include today (to trigger error laster)'
    inst.survey1 = SurveyFactory(datetime_start=datetime.today() + relativedelta(months=-5), datetime_end=datetime.today() + relativedelta(days=-5))
    print inst.survey1
    inst.survey2 = SurveyFactory(datetime_start=datetime.today() + relativedelta(months=-5, years=1), datetime_end=datetime.today() + relativedelta(months=5, years=1))
    print inst.survey2
    inst.survey3 = SurveyFactory(datetime_start=datetime.today() + relativedelta(months=-5, years=2), datetime_end=datetime.today() + relativedelta(months=5, years=2))
    print inst.survey3
    print 'get site mappers'
    site_mappers.autodiscover()
    print 'get one mapper'
    mapper = site_mappers.get(site_mappers.get_as_list()[0])
    inst.community = mapper().get_map_area()
    print 'mapper is {0}'.format(mapper().get_map_area())
    print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
    inst.plot = PlotFactory(community=inst.community)
    inst.household = HouseholdFactory(plot=inst.plot)
    print inst.household.community
    inst.dashboard_type = 'household'
    inst.dashboard_model = 'household'
    inst.dashboard_id = inst.household.pk
