import re
from dateutil.relativedelta import relativedelta
from django import forms
from django.test import TestCase
from bcpp_subject.forms import AccessToCareForm
from datetime import datetime, timedelta
from bhp_lab_tracker.classes import site_lab_tracker
from bhp_registration.models import RegisteredSubject
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_consent.tests.factories import ConsentCatalogueFactory
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from bhp_content_type_map.models import ContentTypeMap
from bhp_content_type_map.classes import ContentTypeMapHelper
from bcpp_subject.models import SubjectConsent
from bcpp_subject.tests.factories import SubjectConsentFactory
from bcpp_survey.tests.factories import SurveyFactory
from bcpp_household.tests.factories import PlotFactory, HouseholdFactory
from bhp_map.classes import site_mappers
from bcpp_household.tests.factories import HouseholdFactory, HouseholdStructureFactory, PlotFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_household_member.models import HouseholdMember
from bcpp_household.models import HouseholdStructure
from bcpp_dashboard.classes import HouseholdDashboard, SubjectDashboard, HtcSubjectDashboard


class ConsentTests(TestCase):

    app_label = 'bcpp_subject'

    def test_p1(self):
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()

        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(model__iexact=SubjectConsent._meta.object_name)
        ConsentCatalogueFactory(
            name=self.app_label,
            content_type_map=content_type_map,
            consent_type='study',
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)

        print 'create survey, plot, household, and household_member'
        print 'create three surveys where NONE include today (to trigger error laster)'
        survey1 = SurveyFactory(datetime_start=datetime.today() + relativedelta(months=-5), datetime_end=datetime.today() + relativedelta(days=-5))
        survey2 = SurveyFactory(datetime_start=datetime.today() + relativedelta(months=-5, years=1), datetime_end=datetime.today() + relativedelta(months=5, years=1))
        survey3 = SurveyFactory(datetime_start=datetime.today() + relativedelta(months=-5, years=2), datetime_end=datetime.today() + relativedelta(months=5, years=2))
        print 'get site mappers'
        site_mappers.autodiscover()
        print 'get one mapper'
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        community = mapper().get_map_area()
        print 'mapper is {0}'.format(mapper().get_map_area())
        print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
        plot = PlotFactory(community=community)
        household = HouseholdFactory(plot=plot)
        print household.community
        dashboard_type = 'household'
        dashboard_model = 'household'
        dashboard_id = household.pk
        print 'initialize the HH dashboard which will create HHS'
        print 'assert no survey for today\'s date'
        self.assertRaises(TypeError, HouseholdDashboard, dashboard_type, dashboard_id, dashboard_model)
        print 'update survey1 to include today'
        survey1.datetime_end = datetime.today() + relativedelta(days=+5)
        survey1.save()
        print 'try again, initialize the HH dashboard which will create HHS'
        household_dashboard = HouseholdDashboard(dashboard_type, dashboard_id, dashboard_model)
        print 'assert household structure exists for this HH and the three surveys'
        self.assertEquals(HouseholdStructure.objects.all().count(), 3)
        household_structure = household_dashboard.get_household_structure()
        print 'create another new HH in community {0}.'.format(community)
        household2 = HouseholdFactory(plot=plot)
        print 'assert no hh structure created'
        self.assertEquals(HouseholdStructure.objects.all().count(), 6)  # 2 surveys for each HH = 2 x 3 = 6
        print 'create HH members for this survey and HH {0}'.format(household)
        hm1 = HouseholdMemberFactory(household_structure=household_structure)
        print 'hm1.registered_subject.pk = {0}'.format(hm1.registered_subject.pk)
        print 'hm1.survey = {0}'.format(hm1.survey)
        hm2 = HouseholdMemberFactory(household_structure=household_structure)
        print hm2.registered_subject.pk
        hm3 = HouseholdMemberFactory(household_structure=household_structure)
        print hm3.registered_subject.pk
        hm4 = HouseholdMemberFactory(household_structure=household_structure)
        print hm4.registered_subject.pk

        # this consent has a fk to registered subject
        # confirm that the signals do not create more than one registered
        # subject or anything like that. consent.rs must equal household_member.rs, etc

        print 'assert one RS per HM'
        self.assertEqual(HouseholdMember.objects.all().count(), RegisteredSubject.objects.all().count())
        print 'assert HM1.registered_subject.subject_identifier is a pk (not consented yet)'
        self.assertRegexpMatches(HouseholdMember.objects.get(pk=hm1.pk).registered_subject.subject_identifier, re_pk)
        print 'consent hm1'
        consent1 = SubjectConsentFactory(household_member=hm1)
        print consent1.subject_identifier
        print HouseholdMember.objects.get(pk=hm1.pk).registered_subject.subject_identifier
        print 'assert consent1 household member is hm1'
        print self.assertEqual(consent1.household_member.pk, hm1.pk)
        print 'assert still one RS per HM'
        self.assertEqual(HouseholdMember.objects.all().count(), RegisteredSubject.objects.all().count())
        print 'assert subject identifier on consent1 == subject identifier in registered_subject'
        self.assertEqual(consent1.subject_identifier, RegisteredSubject.objects.get(subject_identifier=consent1.subject_identifier).subject_identifier)
        print 'assert consent1 registered subject pk = hm1 registered subject pk'
        self.assertEqual(consent1.registered_subject.pk, HouseholdMember.objects.get(pk=hm1.pk).registered_subject.pk)
        print 'assert consent1 registered subject subject identifier = hm1 registered subject subject_identifier'
        self.assertEqual(consent1.registered_subject.subject_identifier, HouseholdMember.objects.get(pk=hm1.pk).registered_subject.subject_identifier)
