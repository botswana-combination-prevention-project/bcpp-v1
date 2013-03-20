from django.conf import settings
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
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


class DashboardTests(TestCase):

    def test_p1(self):
        # setup consent
        # setup bhp_visit
        content_type = ContentType.objects.get(app_label='bhp_consent', model='testsubjectconsent')
        content_type_map = ContentTypeMapFactory(content_type=content_type)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form)
        visit_definition = VisitDefinitionFactory()
        visit_definition.schedule_group.add(schedule_group)
        rs = RegisteredSubject()
        dash = RegisteredSubjectDashboard()
        dash._set_appointments(visit_code=visit_definition.code, visit_instance=None)