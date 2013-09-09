from datetime import datetime
from django.test import TestCase
from bhp_appointment.models import Appointment, PreAppointmentContact
from bhp_visit.tests.factories import VisitDefinitionFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_content_type_map.models import ContentTypeMap
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_lab_tracker.classes import site_lab_tracker
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory


class AuditTrailTests(TestCase):

    def test_audit_trail(self):
        site_lab_tracker.autodiscover()
        StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')

        visit_definition = VisitDefinitionFactory(code='1000', title='Test', visit_tracking_content_type_map=visit_tracking_content_type_map)
        registered_subject = RegisteredSubjectFactory(subject_identifier='12345')
        appointment = Appointment.objects.create(
            appt_datetime=datetime.today(),
            best_appt_datetime=datetime.today(),
            appt_status='new',
            study_site=None,
            visit_definition=visit_definition,
            registered_subject=registered_subject
            )
        # check for the audit trail
        #self.assertTrue(Appointment.history.filter(id=appointment.pk))
        pre_appointment_contact = PreAppointmentContact.objects.create(appointment=appointment, contact_datetime=datetime.today(), is_contacted='Yes', is_confirmed=False)
        #self.assertTrue(PreAppointmentContact.history.filter(id=pre_appointment_contact.pk))
