from bhp_visit.tests.factories import VisitDefinitionFactory
from base_appointment_tests import BaseAppointmentTests
from bhp_appointment.forms import AppointmentForm
from bhp_content_type_map.models import ContentTypeMap


class AppointmentFormTests(BaseAppointmentTests):

    def test_appointment_form(self):
        # create an appointment
        self.setup()
        # confirm visit_instance is 0 for first appointment
        self.assertEqual(self.appointment.visit_instance, '0')
        #self.assertFormError(response, appointment_form, 'appt_datetime', appointment_form.errors, msg_prefix='')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model__iexact='TestVisit')
        visit_definition = VisitDefinitionFactory(id='2', code='9998', title='Test 9998', visit_tracking_content_type_map=visit_tracking_content_type_map)

        appointment_form = AppointmentForm(data={'registered_subject': self.appointment.registered_subject,
                                                 'visit_definition': visit_definition,
                                                 'study_site': self.appointment.study_site,
                                                 'appt_status': 'new',
                                                 'appt_datetime': self.appointment.appt_datetime,
                                                 'appt_type': self.appointment.appt_type,
                                                 'visit_instance': '1'})
        #print self.appointment.__dict__
        #if not appointment_form.is_valid():
        #    print appointment_form.errors
        #self.assertEqual(appointment_form.is_valid(), True)
        self.client.login(username=self.admin_user.username, password='1234')
        response = self.client.post('/admin/bhp_appointment/appointment/', {
            'registered_subject': self.appointment.registered_subject,
            'visit_definition': visit_definition,
            'study_site': self.appointment.study_site,
            'appt_status': 'new',
            #'appt_datetime': self.appointment.appt_datetime,
            'appt_type': self.appointment.appt_type,
            'visit_instance': '1'})
        #print response.content
        #appointment_form.is_valid()
        #self.assertFormError(response, 'AppointmentForm', 'appt_datetime', 'This field is required.')
        self.assertEqual(response.status_code, 200)
        #print response.context.get('error_message')
        #self.assertEqual(response.context['error_message'], 'Cannot create continuation appointment for visit None. Cannot find the original appointment (visit instance equal to 0).')
        #appointment_form.full_clean()
#        appointment_form.data.get('visit_instance')
#        appointment_form.errors
        self.assertContains(response, 'Cannot create continuation appointment for visit None. Cannot find the original appointment (visit instance equal to 0).')
        self.assertEqual(appointment_form.data.get('appt_status'), 'new')
