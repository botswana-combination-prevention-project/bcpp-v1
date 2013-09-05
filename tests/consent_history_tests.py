from django.test import TestCase
from datetime import datetime
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsentHistory
from bhp_base_test.tests.factories import TestConsentFactory, TestConsentHistoryFactory
from bhp_base_test.models import TestConsentHistory


class ConsentUpdateTests(TestCase):

    def test_p1(self):
        print 'create a consent'
        TestConsentFactory(first_name='THING1')
        TestConsentFactory(first_name='THING2')
        TestConsentFactory(first_name='THING3')
        test_consent = TestConsentFactory(first_name='THING4')
        print 'assert has consent history methods'
        self.assertTrue('get_consent_history_model' in dir(test_consent))
        self.assertTrue('update_consent_history' in dir(test_consent))
        self.assertTrue('delete_consent_history' in dir(test_consent))
        print 'confirm RS created'
        self.assertEquals(RegisteredSubject.objects.all().count(), 4)
        self.assertEquals(RegisteredSubject.objects.filter(first_name=test_consent.first_name, dob=test_consent.dob, initials=test_consent.initials).count(), 1)
        print 'assert get_consent_history_model returns a model of base class BaseConsentHistory'
        history_model = test_consent.get_consent_history_model()
        self.assertTrue(issubclass(test_consent.get_consent_history_model(), BaseConsentHistory))
        print 'assert consent history now includes consent for {0}'.format(test_consent)
        self.assertEquals(history_model.objects.filter(registered_subject=test_consent.registered_subject).count(), 1)
        test_consent_history = history_model.objects.get(registered_subject=test_consent.registered_subject, consent_pk=test_consent.pk)
        self.assertEqual(test_consent.consent_datetime, test_consent_history.consent_datetime)
        print 'update consent for {0}'.format(test_consent)
        test_consent.consent_datetime = datetime.today()
        test_consent.save()
        print 'assert history updated for {0}'.format(test_consent)
        test_consent_history = history_model.objects.get(registered_subject=test_consent.registered_subject, consent_pk=test_consent.pk)
        self.assertEqual(test_consent.consent_datetime, test_consent_history.consent_datetime)
        print 'delete consent for {0}'.format(test_consent)
        test_consent.delete()
        print 'assert history update for {0}'.format(test_consent)
        self.assertEqual(history_model.objects.filter(registered_subject=test_consent.registered_subject, consent_pk=test_consent.pk).count(), 0)
        self.assertEqual(history_model.objects.all().count(), 3)
