from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from bhp_variables.models import StudySite
from bhp_appointment.models import Appointment
from bhp_visit.models import VisitDefinition
from bhp_registration.models import RegisteredSubject


class BaseAppointmentTests(TestCase):

    def __init__(self, *args, **kwargs):
        self.visit_definition = None
        self.registered_subject = None
        self.appointment = None
        self.admin_user = None
        super(BaseAppointmentTests, self).__init__(*args, **kwargs)

    def setup(self):
        self.visit_definition = VisitDefinition.objects.create(id='1', code='9999', title='Test')
        self.registered_subject = RegisteredSubject.objects.create(id='1', subject_identifier='062-7982139-3', subject_type='maternal')
        study_site = StudySite.objects.create(site_code='99', site_name='test site')
        self.appointment = Appointment.objects.create(
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
