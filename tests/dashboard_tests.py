from django.conf import settings
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import TestSubjectConsent
from bhp_consent.tests.factories import TestSubjectConsentFactory
from bhp_identifier.exceptions import IdentifierError
from bhp_content_type_map.models import ContentTypeMap
from bhp_content_type_map.tests.factories import ContentTypeMapFactory
from bhp_visit.tests.factories import VisitDefinitionFactory, ScheduleGroupFactory, MembershipFormFactory
from bhp_visit.models import MembershipForm, ScheduleGroup, VisitDefinition
from bhp_dashboard_registered_subject.classes import RegisteredSubjectDashboard
from bhp_lab_tracker.classes import lab_tracker
from lab_requisition.models import TestRequisition
from bhp_visit_tracking.models import TestSubjectVisit


class DashboardTests(TestCase):

    def test_p1(self):
        registered_subject = RegisteredSubjectFactory()
        visit_model = TestSubjectVisit
        requisition_model = TestRequisition
        content_type = ContentType.objects.get(app_label='bhp_consent', model='testsubjectconsent')
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form)
        visit_definition = VisitDefinitionFactory()
        visit_definition.schedule_group.add(schedule_group)
        dashboard = RegisteredSubjectDashboard()
        dashboard.create(dashboard_type='subject',
                         dashboard_identifier='11111111',
                         registered_subject=registered_subject,
                         requisition_model=requisition_model,
                         visit_model=visit_model)

    def test_p2(self):
        lab_tracker.autodiscover()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        # setup consent
        # setup bhp_visit
        content_type = ContentType.objects.get(app_label='bhp_consent', model='testsubjectconsent')
        content_type_map = ContentTypeMap.objects.get(content_type=content_type)
        #content_type_map = ContentTypeMapFactory(content_type=content_type)
        membership_form = MembershipFormFactory(content_type_map=content_type_map, category='subject')
        schedule_group = ScheduleGroupFactory(membership_form=membership_form)
        visit_definition = VisitDefinitionFactory()
        visit_definition.schedule_group.add(schedule_group)
        rs = RegisteredSubjectFactory(subject_type='subject')
        #create appointments
        dash = RegisteredSubjectDashboard()
        print rs.subject_identifier
        dash.create(dashboard_type='subject',
                    dashboard_identifier=rs.subject_identifier,
                    registered_subject=rs,
                    requisition_model=TestRequisition,
                    visit_model=TestSubjectVisit)
        dash._set_appointments(visit_code=visit_definition.code, visit_instance=None)
        print dash._get_membership_form_category()

 