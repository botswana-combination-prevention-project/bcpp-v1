from __future__ import print_function

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from edc.core.bhp_common.utils import convert_from_camel
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.map.classes import site_mappers
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import HouseholdStructure, Household
from bhp066.apps.bcpp_household.tests.factories import HouseholdFactory, PlotFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from .factories import HouseholdMemberFactory


class FormsTests(TestCase):

    app_label = 'bcpp_household_member'

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        plot = PlotFactory(community='test_community3', household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        admin.autodiscover()
        site_lab_tracker.autodiscover()

    def test_all_forms(self):

        adminuser = User.objects.create_user('django', 'django@test.com', 'pass')
        adminuser.save()
        adminuser.is_staff = True
        adminuser.is_active = True
        adminuser.is_superuser = True
        adminuser.save()
        self.client.login(username=adminuser.username, password='pass')

        content_type_map = ContentTypeMap.objects.get(content_type__model='SubjectConsent'.lower())
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='enrollment', grouping_key='ELIGIBILITY')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='subjectvisit')
        visit_definition = VisitDefinitionFactory(code='1000', title='Enrollment', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)

        survey = SurveyFactory()
        site_mappers.autodiscover()
        mapper = site_mappers.get(site_mappers.get_as_list()[0])
        plot = PlotFactory(community=mapper().get_map_area())
        household = HouseholdFactory(plot=plot)
        household_structure = HouseholdStructure.objects.get(household=household, survey=survey)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(household_structure=household_structure)

        n = 0
        # collect inline models
        inline_models = []
        models = []
        for model, model_admin in admin.site._registry.iteritems():
            if self.app_label == model._meta.app_label:
                models.append(model)
                inline_models = inline_models + [m.model for m in model_admin.inlines]
        for model, model_admin in admin.site._registry.iteritems():
            if self.app_label == model._meta.app_label:
                if model in models and model not in inline_models:
                    n += 1
                    model_name = model._meta.object_name
                    url = reverse('admin:{0}_{1}_add'.format(model._meta.app_label, model_name.lower()))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, 'admin/change_form.html')
                    factory_mod = __import__('{0}.tests.factories'.format(self.app_label), fromlist=['{0}Factory'.format(model_name)])
                    factory = getattr(factory_mod, '{0}Factory'.format(model_name))
                    model_instance = factory()
                    url = reverse('admin:{0}_{1}_change'.format(model_instance._meta.app_label, model_instance._meta.object_name.lower()), args=(model_instance.id, ))
                    if model_admin.inlines:
                        for inline_admin in model_admin.inlines:
                            url = reverse('admin:{0}_{1}_add'.format(inline_admin.model._meta.app_label, inline_admin.model._meta.object_name.lower()))
                            response = self.client.get(url)
                            self.assertEqual(response.status_code, 200)
                            self.assertTemplateUsed(response, 'admin/change_form.html')
                            factory_mod = __import__('bcpp_subject.tests.factories', fromlist=['{0}Factory'.format(inline_admin.model._meta.object_name)])
                            factory = getattr(factory_mod, '{0}Factory'.format(inline_admin.model._meta.object_name))
                            factory(**{convert_from_camel(model_instance._meta.object_name): model_instance, 'subject_visit': model_instance.subject_visit})
                            factory(**{convert_from_camel(model_instance._meta.object_name): model_instance, 'subject_visit': model_instance.subject_visit})

                    response = self.client.post(url, model_instance.__dict__)
                    self.assertEqual(response.status_code, 200)
