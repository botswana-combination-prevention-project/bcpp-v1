from datetime import datetime
from django.test import TestCase
from bhp_appointment.models import Appointment, PreAppointmentContact
from bhp_visit.tests.factories import VisitDefinitionFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory


class AuditTrailTests(TestCase):

    fixtures = ['test_configuration.json']

    def test_audit_trail(self):
        # save an appointment
        visit_definition = VisitDefinitionFactory(code='1000', title='Test')
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
        self.assertTrue(Appointment.history.filter(id=appointment.pk))
        pre_appointment_contact = PreAppointmentContact.objects.create(appointment=appointment, contact_datetime=datetime.today(), is_contacted='Yes', is_confirmed=False)
        self.assertTrue(PreAppointmentContact.history.filter(id=pre_appointment_contact.pk))
