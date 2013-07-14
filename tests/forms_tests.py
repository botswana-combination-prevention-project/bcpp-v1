from __future__ import print_function
from datetime import datetime
from django.contrib import admin
from django.test import TestCase
from django.db.models import get_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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

        for model_admin in admin.site._registry:
            if self.app_label == model_admin._meta.app_label:
                m = get_model(model_admin._meta.app_label, model_admin._meta.object_name)
                if issubclass(m, BaseScheduledVisitModel):
                    model_name = model_admin._meta.object_name
                    print('{0}_{1}_add'.format(model_admin._meta.app_label, model_name.lower()))
                    url = reverse('admin:{0}_{1}_add'.format(model_admin._meta.app_label, model_name.lower()))
                    response = self.client.get(url)
                    print('  assert response=200')
                    self.assertEqual(response.status_code, 200)
                    print('  assert template')
                    self.assertTemplateUsed(response, 'admin/change_form.html')
                    factory_mod = __import__('bcpp_subject.tests.factories', fromlist=['{0}Factory'.format(model_name)])
                    factory = getattr(factory_mod, '{0}Factory'.format(model_name))
                    print('  instantiate the factory')
                    model = factory(subject_visit=subject_visit)
                    print('  subject_visit = {0}'.format(model.subject_visit))
                    print('  get admin change url for pk={0}'.format(model.id))
                    url = reverse('admin:{0}_{1}_change'.format(model_admin._meta.app_label, model_admin._meta.object_name.lower()), args=(model.id, ))
                    print('  url = {0}'.format(url))
                    print('  subject_visit.get_subject_identifier() = {0}'.format(model.subject_visit.get_subject_identifier()))
                    print('  post url')
                    response = self.client.post(url, )
