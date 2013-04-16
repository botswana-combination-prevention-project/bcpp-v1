from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from bhp_variables.tests.factories import StudySiteFactory
from bhp_appointment.tests.factories import AppointmentFactory
from bhp_visit.tests.factories import VisitDefinitionFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory


class BaseAppointmentTests(TestCase):

    def __init__(self, *args, **kwargs):
        self.visit_definition = None
        self.registered_subject = None
        self.appointment = None
        self.admin_user = None
        super(BaseAppointmentTests, self).__init__(*args, **kwargs)

    def setup(self):
        self.visit_definition = VisitDefinitionFactory(code='9999', title='Test')
        self.registered_subject = RegisteredSubjectFactory(subject_identifier='062-7982139-3', subject_type='maternal')
        study_site = StudySiteFactory(site_code='99', site_name='test site')
        self.appointment = AppointmentFactory(
            appt_datetime=datetime.today(),
            best_appt_datetime=datetime.today(),
            appt_status='new',
            study_site=study_site,
            visit_definition=self.visit_definition,
            registered_subject=self.registered_subject,
            )
        # create a admin_user
        self.admin_user = User.objects.create(username='admin', password='1234')
        self.admin_user.set_password('1234')
        self.admin_user.is_staff = True
        self.admin_user.is_active = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
