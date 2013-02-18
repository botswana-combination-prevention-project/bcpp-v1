from datetime import datetime
from django.core.exceptions import ValidationError
from bhp_appointment.choices import APPT_STATUS
from bhp_appointment.models import Appointment
from bhp_visit.models import VisitDefinition
from base_appointment_tests import BaseAppointmentTests


class AppointmentMethodTests(BaseAppointmentTests):

    fixtures = ['test_configuration.json']

    def test_save(self):
        # create an appointment
        self.setup()
        # confirm visit_instance is 0 for first appointment
        self.assertEqual(self.appointment.visit_instance, '0')
        #try to change the visit instnce of the existing appointment to 1
        self.appointment.visit_instance = '1'
        # expect a validation error, because there is no appt with visit_instance == 0
        self.assertRaises(ValidationError, self.appointment.save)
        # put visit_instance back to 0
        self.appointment.visit_instance = '0'
        try:
            self.appointment.save()
        except:
            self.fail('appointment.save() has unexpectedly raised an exception.')
        self.assertEqual(self.appointment.visit_instance, '0')
        # create another appt with the same visit definition, skip an instance, expect a ValidationError
        self.appointment = Appointment(
                appt_datetime=datetime.today(),
                best_appt_datetime=datetime.today(),
                appt_status='new',
                study_site=None,
                visit_definition=self.visit_definition,
                registered_subject=self.registered_subject,
                visit_instance='2',
                )
        self.assertRaises(ValidationError, self.appointment.save)
        # set visit_instance to 1 and expect it to save without an exception
        self.appointment.visit_instance = '1'
        try:
            self.appointment.save()
        except:
            self.fail('appointment.save() has unexpectedly raised an exception.')

    def test_is_new_appointment(self):
        """
        is_new_appointment() should return False if not "new" and "new" must be listed in the choices tuple.
        """
        appointment = Appointment()
        dte = datetime.today()
        appointment.appt_datetime = dte
        self.assertEqual(appointment.is_new_appointment(), True, 'Expected is_new_appointment() to return True for appt_status=\'{0}\'. Got \'{1}\''.format(appointment.appt_status, appointment.is_new_appointment()))
        appointment.appt_status = 'Done'
        self.assertEqual(appointment.is_new_appointment(), False, 'Expected is_new_appointment() to return False for appt_status=\'{0}\'. Got \'{1}\''.format(appointment.appt_status, appointment.is_new_appointment()))
        is_found_new = False
        for choice in APPT_STATUS:
            appointment.appt_status = choice[0]
            if appointment.appt_status == 'new':
                # flag to show "new" exists in tuple
                is_found_new = True
                self.assertEqual(appointment.is_new_appointment(), True)
            else:
                # all other cases return False
                self.assertEqual(appointment.is_new_appointment(), False)
        # test "new" case exists in choices
        self.assertEqual(is_found_new, True)

    def test_validate_appt_datetime(self):

        # a new record, original appt_datetime and best_appt_datetime are equal. 
        appointment = Appointment()
        dte = datetime.today()
        appointment.appt_datetime = dte
        # returned appt_datetime may not be equal to original appt_datetime
        appt_datetime, appointment.best_appt_datetime = appointment.validate_appt_datetime()
        self.assertEqual(appointment.appt_datetime, appointment.best_appt_datetime, 'Expected appointment.appt_datetime and best_appt_datetime to be equal.')

        # a changed record must return  appt_datetime and best_appt_datetime but they do not need to be equal
        appointment.id = '1'
        appointment.appt_datetime = appt_datetime
        appointment.study_site = None
        appointment.visit_definition = VisitDefinition(code='1000', title='Test')
        appt_datetime, best_appt_datetime = appointment.validate_appt_datetime()
        self.assertEqual(appt_datetime == None, False)
        self.assertEqual(best_appt_datetime == None, False)
