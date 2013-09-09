from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from bhp_dashboard.classes import Dashboard
from bhp_dashboard.exceptions import DashboardModelError
from bhp_registration.models import RegisteredSubject
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_base_test.models import TestConsent, TestVisit
from bhp_base_test.tests.factories import TestConsentFactory


class DashboardMethodTests(TestCase):

    def test_p1(self):
        test_consent = TestConsentFactory()
        registered_subject = test_consent.registered_subject
        print registered_subject.first_name
        self.assertRaises(TypeError, Dashboard)
        self.assertRaises(TypeError, Dashboard, None, None, None)
        self.assertRaises(TypeError, Dashboard, 'subject', None, None)
        self.assertRaises(TypeError, Dashboard, 'subject', '--', None)
        self.assertRaises(TypeError, Dashboard, 'subject', '--', RegisteredSubject)
        self.assertRaises(TypeError, Dashboard, 'subject', registered_subject.pk, RegisteredSubject)

        print 'assert OK if registered_subject is the dashboard model and is specified as model class'
        dashboard = Dashboard('subject', registered_subject.pk, RegisteredSubject, dashboard_type_list=['subject'])
        self.assertEquals(dashboard.get_dashboard_type(), 'subject')
        self.assertEquals(dashboard.get_dashboard_models(), {'registered_subject': RegisteredSubject})
        print 'assert correctly updates instead of adds to dictionary of added twice'
        dashboard.add_dashboard_model({'registered_subject': RegisteredSubject})
        self.assertEquals(dashboard.get_dashboard_model(), RegisteredSubject)
        self.assertEquals(dashboard.get_dashboard_id(), registered_subject.pk)
        self.assertEquals(dashboard.get_dashboard_model_name(), 'registered_subject')

        print 'assert OK if registered_subject is the dashboard model and is specified as a model_name instead of class'
        dashboard = Dashboard('subject', registered_subject.pk, 'registered_subject', dashboard_type_list=['subject'])
        self.assertEquals(dashboard.get_dashboard_type(), 'subject')
        self.assertRaises(TypeError, dashboard.get_dashboard_model, RegisteredSubject)
        dashboard.add_dashboard_model({'registered_subject': RegisteredSubject})
        self.assertEquals(dashboard.get_dashboard_model(), RegisteredSubject)
        self.assertEquals(dashboard.get_dashboard_id(), registered_subject.pk)
        self.assertEquals(dashboard.get_dashboard_model_name(), 'registered_subject')

        print 'assert raises TypeErrors if incomplete parameter list'
        #registered_subject = RegisteredSubjectFactory()
        #print registered_subject.first_name
        test_consent = TestConsentFactory()
        self.assertRaises(TypeError, Dashboard)
        self.assertRaises(TypeError, Dashboard, None, None, None)
        self.assertRaises(TypeError, Dashboard, 'subject', None, None)
        self.assertRaises(TypeError, Dashboard, 'subject', '--', None)
        self.assertRaises(TypeError, Dashboard, 'subject', '--', RegisteredSubject)
        self.assertRaises(TypeError, Dashboard, 'subject', test_consent.pk, TestConsent)

        print 'assert raises exception if dashboard model is not in dictionary'
        self.assertRaises(DashboardModelError, Dashboard, 'subject', test_consent.pk, TestConsent, dashboard_type_list=['subject'])
        print 'assert OK if dashboard model is added to dictionary using the dashboard instance'
        dashboard.add_dashboard_model({'test_consent': TestConsent})
        self.assertIn('test_consent', dashboard.get_dashboard_models())
        print 'assert OK if dashboard model is specified (and added) at init instead of on the dashboard instance'
        
        class D1(Dashboard):
            dashboard_url_name = 'subject_dashboard_url'

        dashboard = D1(
            'subject',
            test_consent.pk,
            TestConsent,
            dashboard_type_list=['subject'],
            dashboard_models={'test_consent': TestConsent})
        self.assertEquals(dashboard.get_dashboard_type(), 'subject')
        self.assertRaises(TypeError, dashboard.get_dashboard_model, TestConsent)
        self.assertEquals(dashboard.get_dashboard_model(), TestConsent)
        self.assertEquals(dashboard.get_dashboard_id(), test_consent.pk)
        self.assertEquals(dashboard.get_dashboard_model_name(), 'test_consent')

        print 'assert can add a model to the dashboard model list'
        dashboard = Dashboard(
            'subject',
            test_consent.pk,
            'test_consent',
            dashboard_type_list=['subject'],
            dashboard_models={'test_consent': TestConsent})
        self.assertIn('test_consent', dashboard.get_dashboard_models())
        self.assertEquals(dashboard.get_dashboard_type(), 'subject')
        self.assertRaises(TypeError, dashboard.get_dashboard_model, TestConsent)
        dashboard.add_dashboard_model({'test_consent': TestConsent})
        self.assertEqual(sorted(['test_consent', 'registered_subject']), sorted(dashboard.get_dashboard_models()))
        self.assertEquals(dashboard.get_dashboard_model(), TestConsent)
        self.assertEquals(dashboard.get_dashboard_id(), test_consent.pk)
        self.assertEquals(dashboard.get_dashboard_model_name(), 'test_consent')
        self.assertTrue(isinstance(dashboard.get_dashboard_model_instance(), TestConsent))

        print 'assert can convert a dashboard_model_list item from a function'

        def get_visit_model():
            return TestVisit

        dashboard = D1(
            'subject',
            test_consent.pk,
            'test_consent',
            dashboard_type_list=['subject'],
            dashboard_models={'test_consent': TestConsent, 'test_visit': get_visit_model})
        self.assertIn('test_consent', dashboard.get_dashboard_models())
        self.assertEquals(dashboard.get_dashboard_type(), 'subject')
        dashboard.add_dashboard_model({'test_consent': TestConsent})
        self.assertEqual(sorted(['test_consent', 'registered_subject', 'test_visit']), sorted(dashboard.get_dashboard_models()))
        self.assertEquals(dashboard.get_dashboard_model(), TestConsent)
        self.assertEquals(dashboard.get_dashboard_id(), test_consent.pk)
        self.assertEquals(dashboard.get_dashboard_model_name(), 'test_consent')
        self.assertTrue(isinstance(dashboard.get_dashboard_model_instance(), TestConsent))

        print 'assert can convert a dashboard_model_list item from a method'

        class Obj(object):
            def get_visit_model(self):
                return TestVisit

        dashboard = D1(
            'subject',
            test_consent.pk,
            'test_consent',
            dashboard_type_list=['subject'],
            dashboard_models={'test_consent': TestConsent, 'test_visit': Obj().get_visit_model})
        self.assertIn('test_consent', dashboard.get_dashboard_models())
        self.assertEquals(dashboard.get_dashboard_type(), 'subject')
        dashboard.add_dashboard_model({'test_consent': TestConsent})
        self.assertEqual(sorted(['test_consent', 'registered_subject', 'test_visit']), sorted(dashboard.get_dashboard_models()))
        self.assertEquals(dashboard.get_dashboard_model(), TestConsent)
        self.assertEquals(dashboard.get_dashboard_id(), test_consent.pk)
        self.assertEquals(dashboard.get_dashboard_model_name(), 'test_consent')
        self.assertTrue(isinstance(dashboard.get_dashboard_model_instance(), TestConsent))

        print 'assert method verify_dashboard_model'

        class Obj2(object):
            def get_visit_model(self):
                return TestVisit

        class D2(Dashboard):

            dashboard_url_name = 'subject_dashboard_url'

            def verify_dashboard_model(self, model):
                if model:
                    if not 'get_registered_subject_blah_blah' in dir(model):
                        raise ImproperlyConfigured('Dashboard model must have method get_registered_subject_blah_blah().')

        self.assertRaisesRegexp(ImproperlyConfigured, 'get_registered_subject_blah_blah', D2,
            'subject',
            test_consent.pk,
            'test_consent',
            dashboard_type_list=['subject'],
            dashboard_models={'test_consent': TestConsent, 'test_visit': Obj2().get_visit_model})

        dashboard = D1(
            'subject',
            test_consent.pk,
            'test_consent',
            dashboard_type_list=['subject'],
            dashboard_models={'test_consent': TestConsent, 'test_visit': Obj().get_visit_model})

        print 'get_context'
        dashboard.get_context()
        self.assertEqual(dashboard.context.get().get('dashboard_type'), 'subject')
        self.assertEqual(dashboard.context.get().get('dashboard_id'), test_consent.pk)
        self.assertEqual(dashboard.context.get().get('dashboard_model'), 'test_consent')
        self.assertEqual(dashboard.context.get().get('dashboard_model_instance'), test_consent)
        self.assertEqual(sorted(dashboard.context.get().keys()), sorted(['app_label', 'dashboard_id', 'dashboard_model', 'dashboard_model_instance', 'dashboard_type', 'dashboard_name', 'dashboard_url_name', 'hostname', 'os_variables', 'template']))
