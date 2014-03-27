from datetime import datetime
from django.db import IntegrityError
from django.contrib import admin
from django.test import TestCase
from django.contrib.auth.models import User
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.map.classes import site_mappers
from apps.bcpp_survey.tests.factories import SurveyFactory
from apps.bcpp_subject.models import SubjectConsent
from apps.bcpp_household.tests.factories import HouseholdStructureFactory, PlotFactory, HouseholdFactory
from apps.bcpp_household.models import HouseholdStructure, Household
from .factories import HouseholdMemberFactory


class HouseholdCompositionTests(TestCase):

    app_label = 'bcpp_household_member'

    def test_p1(self):
        admin.autodiscover()
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()

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

        adminuser = User.objects.create_user('django', 'django@test.com', 'pass')
        adminuser.save()
        adminuser.is_staff = True
        adminuser.is_active = True
        adminuser.is_superuser = True
        adminuser.save()
        self.client.login(username=adminuser.username, password='pass')

        print 'create a survey'
        survey1 = SurveyFactory()
        survey2 = SurveyFactory()
        print 'get site mappers'
        site_mappers.autodiscover()
        print 'get one mapper'
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        print 'mapper is {0}'.format(mapper().get_map_area())
        print 'create a plot model instance for community {0}'.format(mapper().get_map_area())
        self.assertEqual(Household.objects.all().count(), 0)
        print 'Create a plot'
        plot = PlotFactory(community=mapper().get_map_area())
        plot.save()
        print 'create a household on this plot for survey={0}'.format(survey1)
        household = HouseholdFactory(plot=plot)
        print 'assert hs created'
        self.assertRaises(IntegrityError, HouseholdStructureFactory, household=household, survey=survey1)
        household_structure1 = HouseholdStructure.objects.get(household=household, survey=survey1)
        print 'add members'
        hm1 = HouseholdMemberFactory(household_structure=household_structure1, first_name='ERIK', initials='EW')
        hm2 = HouseholdMemberFactory(household_structure=household_structure1, first_name='ERIK', initials='E1W')
        hm3 = HouseholdMemberFactory(household_structure=household_structure1, first_name='ERIK', initials='E2W')
        print 'change members'
        hm1.save()
        hm2.save()
        hm3.save()
        print 'resave household on this plot for survey={0}'.format(survey2)
        household.save()
        self.assertRaises(IntegrityError, HouseholdStructureFactory, household=household, survey=survey2)
        household_structure2 = HouseholdStructure.objects.get(household=household, survey=survey2)
        print 'assert using different hs'
        self.assertNotEqual(household_structure1, household_structure2)
        print 'add members'
        HouseholdMemberFactory(household_structure=household_structure2)
        HouseholdMemberFactory(household_structure=household_structure2, first_name='ERIK', initials='E1W')
        HouseholdMemberFactory(household_structure=household_structure2, first_name='ERIK', initials='E2W')
        HouseholdMemberFactory(household_structure=household_structure2, first_name='ERIK', initials='EW')
        print 'change members'
        hm1.save()
        hm2.save()
        hm3.save()
