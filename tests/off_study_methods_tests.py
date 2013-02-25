from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_content_type_map.models import ContentTypeMap
from bhp_registration.models import RegisteredSubject
from bhp_appointment.models import Appointment, Configuration
from bhp_visit.models import VisitDefinition
from bhp_consent.models import TestSubjectConsent, ConsentCatalogue, AttachedModel
from bhp_variables.models import StudySite
from bhp_off_study.models import TestOffStudy


class OffStudyMethodsTests(TestCase):

    def setUp(self):
        study_site = StudySite.objects.create(site_code='10', site_name='TESTSITE')
        Configuration.objects.create()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(model__iexact=TestSubjectConsent._meta.object_name)
        consent_catalogue = ConsentCatalogue.objects.create(
            name='test',
            content_type_map=content_type_map,
            consent_type='study',
            version=1,
            start_datetime=datetime.today() - relativedelta(months=7),
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app='bhp_off_study')
        consent_catalogue.add_for_app = 'bhp_consent'
        consent_catalogue.save()
        # assert OffStudy model is in AttachedModel
        self.assertTrue(AttachedModel.objects.get(content_type_map=ContentTypeMap.objects.get(model__iexact=TestOffStudy._meta.object_name)))
        # create a subject
        self.registered_subject = RegisteredSubject.objects.create()
        # consent the subject
        self.subject_consent = TestSubjectConsent.objects.create(
            first_name='TEST',
            last_name='TESTER',
            initials='TT',
            identity='111111111',
            confirm_identity='111111111',
            identity_type='omang',
            dob=datetime(1990, 01, 01),
            is_dob_estimated='No',
            gender='M',
            subject_type='subject',
            consent_datetime=datetime.today(),
            study_site=study_site,
            may_store_samples='Yes',
            )
        # create some visit definitions
        VisitDefinition.objects.create(code='1000')
        VisitDefinition.objects.create(code='1300')
        VisitDefinition.objects.create(code='1600')
        VisitDefinition.objects.create(code='1800')

    def test_post_save(self):
        # create some appointments
        now = datetime.today()
        for visit_code, dte in {'1000': now - relativedelta(months=6), '1300': now - relativedelta(months=3), '1600': now, '1800': now + relativedelta(months=3)}.iteritems():
            Appointment.objects.create(registered_subject=self.registered_subject, appt_datetime=dte, visit_definition=VisitDefinition.objects.get(code=visit_code))
        # create off study with date before last appointment
        TestOffStudy.objects.create(registered_subject=self.registered_subject, offstudy_date=date(now.year, now.month, now.day))
        self.assertTrue(Appointment.objects.filter(appt_datetime=now - relativedelta(months=6)).exists())
        self.assertTrue(Appointment.objects.filter(appt_datetime=now - relativedelta(months=3)).exists())
        self.assertTrue(Appointment.objects.filter(appt_datetime=now).exists())
        # assert last appointment does not exist
        self.assertFalse(Appointment.objects.filter(appt_datetime=now + relativedelta(months=6)).exists())
