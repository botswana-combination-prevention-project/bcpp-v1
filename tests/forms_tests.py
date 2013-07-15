from __future__ import print_function
from datetime import datetime
from django.contrib import admin
from django.test import TestCase
from django.db.models import get_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from bhp_common.utils import convert_from_camel
from bhp_lab_tracker.classes import lab_tracker
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_consent.tests.factories import ConsentCatalogueFactory
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from bhp_content_type_map.models import ContentTypeMap
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_appointment.tests.factories import AppointmentFactory
from bhp_visit.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from bcpp_household.tests.factories import HouseholdFactory, HouseholdStructureFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory
from bcpp_subject.models import SubjectConsent
from bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory, EnrolmentChecklistFactory
from bcpp_subject.models import BaseScheduledVisitModel

admin.autodiscover()


class FormsTests(TestCase):

    app_label = 'bcpp_subject'

    def test_all_forms(self):
        lab_tracker.autodiscover()
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

        adminuser = User.objects.create_user('django', 'django@test.com', 'pass')
        adminuser.save()
        adminuser.is_staff = True
        adminuser.is_active = True
        adminuser.is_superuser = True
        adminuser.save()
        self.client.login(username=adminuser.username, password='pass')

        content_type_map = ContentTypeMap.objects.get(content_type__model='EnrolmentChecklist'.lower())
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='enrolment', grouping_key='ELIGIBILITY')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='subjectvisit')
        visit_definition = VisitDefinitionFactory(code='1000', title='Enrolment', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)

        survey = SurveyFactory()
        household = HouseholdFactory()
        household_structure = HouseholdStructureFactory(household=household, survey=survey)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        HouseholdMemberFactory(household_structure=household_structure)
        household_member = HouseholdMemberFactory(household_structure=household_structure)

        subject_consent = SubjectConsentFactory(household_member=household_member)
        print(subject_consent.registered_subject)
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        self.assertEqual(subject_consent.registered_subject.pk, registered_subject.pk)

        enrolment = EnrolmentChecklistFactory(registered_subject=registered_subject)

        self.assertEqual(Appointment.objects.all().count(), 1)
        appointment = Appointment.objects.get(registered_subject=registered_subject)
        self.assertEqual(appointment.registered_subject.pk, registered_subject.pk)

        subject_visit = SubjectVisitFactory(appointment=appointment)
        n = 0
        # collect inline models
        inline_models = []
        for model, model_admin in admin.site._registry.iteritems():
            if self.app_label == model._meta.app_label:
                inline_models = inline_models + [m.model for m in model_admin.inlines]
        print('Inline models are {0}'.format(', '.join([m._meta.object_name for m in inline_models])))
        for model, model_admin in admin.site._registry.iteritems():
            if self.app_label == model._meta.app_label:
                if issubclass(model, BaseScheduledVisitModel) and model not in inline_models:
                    n += 1
                    model_name = model._meta.object_name
                    print('{0}_{1}_add'.format(model._meta.app_label, model_name.lower()))
                    url = reverse('admin:{0}_{1}_add'.format(model._meta.app_label, model_name.lower()))
                    response = self.client.get(url)
                    print('  assert response=200')
                    self.assertEqual(response.status_code, 200)
                    print('  assert template')
                    self.assertTemplateUsed(response, 'admin/change_form.html')
                    factory_mod = __import__('bcpp_subject.tests.factories', fromlist=['{0}Factory'.format(model_name)])
                    factory = getattr(factory_mod, '{0}Factory'.format(model_name))
                    print('  instantiate the factory')
                    model_instance = factory(subject_visit=subject_visit)
                    print('  subject_visit = {0}'.format(model_instance.subject_visit))
                    print('  get admin change url for pk={0}'.format(model_instance.id))
                    url = reverse('admin:{0}_{1}_change'.format(model_instance._meta.app_label, model_instance._meta.object_name.lower()), args=(model_instance.id, ))
                    print('  url = {0}'.format(url))
                    print('  subject_visit.get_subject_identifier() = {0}'.format(model_instance.subject_visit.get_subject_identifier()))
                    if model_admin.inlines:
                        for inline_admin in model_admin.inlines:
                            print('  inline model {0}'.format(inline_admin.model))
                            print('    {0}_{1}_add'.format(inline_admin.model._meta.app_label, inline_admin.model._meta.object_name.lower()))
                            url = reverse('admin:{0}_{1}_add'.format(inline_admin.model._meta.app_label, inline_admin.model._meta.object_name.lower()))
                            response = self.client.get(url)
                            print('    assert response=200')
                            self.assertEqual(response.status_code, 200)
                            print('    assert template')
                            self.assertTemplateUsed(response, 'admin/change_form.html')
                            factory_mod = __import__('bcpp_subject.tests.factories', fromlist=['{0}Factory'.format(inline_admin.model._meta.object_name)])
                            factory = getattr(factory_mod, '{0}Factory'.format(inline_admin.model._meta.object_name))
                            print('    instantiate the factory {0}'.format(factory))
                            factory(**{convert_from_camel(model_instance._meta.object_name): model_instance, 'subject_visit': model_instance.subject_visit})
                            factory(**{convert_from_camel(model_instance._meta.object_name): model_instance, 'subject_visit': model_instance.subject_visit})

                    #print('  post url')
                    #response = self.client.post(url, )
        print('tested {0} forms'.format(n))
