from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment
from bhp_visit.models import VisitDefinition
from bhp_off_study.models import TestOffStudy


class OffStudyMethodsTests(TestCase):

    def test_post_save(self):
        # create a subject
        registered_subject = RegisteredSubject.objects.create()
        # create some visit definitions
        VisitDefinition.objects.create(code='1000')
        VisitDefinition.objects.create(code='1300')
        VisitDefinition.objects.create(code='1600')
        VisitDefinition.objects.create(code='1800')
        # create some appointments
        now = datetime.today()
        for visit_code, dte in {'1000': now - relativedelta(months=6), '1300': now - relativedelta(months=3), '1600': now, '1800': now + relativedelta(months=3)}.iteritems():
            Appointment.objects.create(appt_datetime=dte, visit_definition=VisitDefinition.objects.get(code=visit_code))
        # create off study with date before last appointment
        TestOffStudy.objects.create(off_study_datetime=now)
        # assert last appointment does not exist
        self.assertFalse(Appointment.objects.filter(appt_datetime=now + relativedelta(months=6).exists()))
