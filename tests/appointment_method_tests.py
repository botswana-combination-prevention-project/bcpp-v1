from datetime import datetime
from django.core.exceptions import ValidationError
from bhp_appointment.choices import APPT_STATUS
from bhp_appointment.models import Appointment
from bhp_visit.models import VisitDefinition
from base_appointment_tests import BaseAppointmentTests
from django.test import TestCase
from django.db.models import get_app, get_models
from bhp_identifier.exceptions import IdentifierError
from bhp_lab_tracker.classes import lab_tracker
from bhp_variables.models import StudySpecific, StudySite
from bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from bhp_registration.models import RegisteredSubject
from bhp_consent.tests.factories import ConsentCatalogueFactory
from bhp_appointment.models import Appointment
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_visit.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_content_type_map.models import ContentTypeMap
from bhp_identifier.models import SubjectIdentifier, Sequence
from bhp_off_study.exceptions import SubjectOffStudyError, SubjectOffStudyDateError
from bhp_base_test.models import TestConsent, TestRegistration, TestVisit
from bhp_base_test.tests.factories import TestRegistrationFactory, TestVisitFactory, TestConsentFactory
from bhp_appointment.exceptions import AppointmentStatusError


class AppointmentMethodTests(BaseAppointmentTests):
    #fixtures = ['test_configuration.json', 'test_variables.json']

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
        lab_tracker.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()

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

    def test_validate_appt_status(self):
        # setup visit 1000
        app_label = 'bhp_base_test'
        lab_tracker.autodiscover()
        StudySpecificFactory()
        study_site = StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        print 'setup the consent catalogue for app {0}'.format(app_label)
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestConsent._meta.object_name.lower())
        consent_catalogue = ConsentCatalogueFactory(name='v1', content_type_map=content_type_map)
        consent_catalogue.add_for_app = 'bhp_base_test'
        consent_catalogue.save()

        print 'setup bhp_visit'
        content_type_map = ContentTypeMap.objects.get(content_type__model=TestRegistration._meta.object_name.lower())
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model=TestVisit._meta.object_name.lower())
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='Test Reg', grouping_key='REGISTRATION')
        visit_definition = VisitDefinitionFactory(code='1000', title='Test Registration', grouping='test_subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)

        # add consent
        test_consent = TestConsentFactory()
        # add registration
        registered_subject = RegisteredSubject.objects.get(subject_identifier=test_consent.subject_identifier)
        self.assertEquals(Appointment.objects.all().count(), 0)
        # complete a registration forms
        test_registration = TestRegistrationFactory(registered_subject=registered_subject)
        self.assertEquals(Appointment.objects.all().count(), 1)
        # get an appointment
        appointment = Appointment.objects.get(registered_subject=registered_subject, visit_definition__code='1000')
        self.assertEqual(appointment.appt_status, 'new')
        print 'update appointment and save, assert reverts to New or Cancelled when no visit tracking'
        for appt_status in APPT_STATUS:
            appointment.appt_status = appt_status[0]
            appointment.save()
            if appt_status == 'cancelled':
                self.assertIn(appointment.appt_status, ['cancelled'])
            else:
                self.assertIn(appointment.appt_status, ['new', 'cancelled'])
        print 'add a visit tracking form'
        test_visit = TestVisitFactory(appointment=appointment, reason='scheduled')
        self.assertEquals(appointment.appt_status, 'in_progress')
        print 'with a \'scheduled\' visit tracking form, update appointment and save, assert reverts to New or Cancelled'
        print 'confirm appt_status can only be \'in_progress\''
        for appt_status in APPT_STATUS:
            appointment = Appointment.objects.get(registered_subject=registered_subject, visit_definition__code='1000', visit_instance='0')
            print 'appointment status is {0}'.format(appointment.appt_status)
            self.assertEquals(Appointment.objects.all().count(), 1)
            appointment.appt_status = appt_status[0]
            appointment.save()
            print 'change appointment status to {0}'.format(appt_status[0])
            if appt_status[0] == 'cancelled':
                self.assertRaises(AppointmentStatusError, appointment.save)
            elif appt_status[0] == 'new':
                self.assertRaises(AppointmentStatusError, appointment.save)
            elif appt_status[0] == 'in_progress':
                self.assertEquals(appointment.appt_status, 'in_progress')
            elif appt_status[0] == 'done':
                self.assertRaises(AppointmentStatusError, appointment.save)
            elif appt_status[0] == 'incomplete':
                self.assertEquals(appointment.appt_status, 'incomplete')
            else:
                raise TypeError()

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
