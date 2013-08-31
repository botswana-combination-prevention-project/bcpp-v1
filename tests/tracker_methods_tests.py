from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_variables.tests.factories import StudySpecificFactory
from bhp_lab_tracker.classes import LabTracker, site_lab_tracker
from bhp_lab_tracker.classes.controller import AlreadyRegistered
from lab_clinic_api.models import ResultItem
from bhp_base_test.models import TestSubjectResultModel
from bhp_base_test.tests.factories import TestSubjectResultModelFactory, TestVisitFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_appointment.tests.factories import AppointmentFactory
from bhp_lab_tracker.models import HistoryModel
from lab_clinic_api.tests.factories import ResultItemFactory, AliquotConditionFactory, AliquotFactory, OrderFactory, ReceiveFactory, ResultFactory, TestCodeFactory


class TrackerMethodsTests(TestCase):

    def test_p1(self):
        StudySpecificFactory()
        ConfigurationFactory()
        print 'assert not yet autodiscovered'
        site_lab_tracker._registry = []
        self.assertEqual(site_lab_tracker._registry, [])
        tracker = LabTracker()
        self.assertEqual(tracker.trackers, None)
        # get models, sets the model
        self.assertTrue(isinstance(tracker.get_trackers(), list))
        # at least result item is included
        self.assertEquals(len(tracker.get_trackers()), 1)
        self.assertEquals(tracker.get_trackers()[0][0], ResultItem)
        del tracker

        class TestLabTracker(LabTracker):
            subject_type = 'test_subject_type'
            trackers = [(TestSubjectResultModel, 'result', 'result_datetime', )]
            group_name = 'HIV'
            tracked_test_codes = ('HIV', 'ELISA', 'RELISA')

        subject_identifier = 'subject_identifier1'
        subject_type = 'test_subject_type'
        tracker1 = TestLabTracker(subject_identifier)
        self.assertNotEqual(tracker1.trackers, None)
        # get models, sets the model
        self.assertTrue(isinstance(tracker1.get_trackers(), list))
        # at least result item is included
        self.assertEquals(len(tracker1.get_trackers()), 2)
        trackers = [tracker_tpl[0] for tracker_tpl in tracker1.get_trackers()]
        self.assertTrue(ResultItem in trackers)
        self.assertTrue(TestSubjectResultModel in trackers)
        value_datetime = datetime.today() - timedelta(days=5)
        group_name = 'HIV'

        print 'test if no history yet available, returns default value (UNK)'
        self.assertEqual(tracker1.get_history(value_datetime).count(), 0)
        self.assertEqual('UNK', tracker1.get_value(value_datetime))
        self.assertTrue(isinstance(tracker1._get_history_inst(), HistoryModel))
        self.assertTrue(tracker1._get_history_inst().subject_identifier, subject_identifier)
        self.assertTrue(tracker1._get_history_inst().value_datetime, value_datetime)
        self.assertTrue(tracker1._get_history_inst().value, 'UNK')
        self.assertTrue(tracker1._get_history_inst().pk == '')

        print 'add a TestModelResult with a POS result value to the tracker model'
        self.assertEqual(tracker1.get_history(value_datetime).count(), 0)
        test_result_model = TestSubjectResultModelFactory(subject_identifier=subject_identifier, result='POS', result_datetime=value_datetime)
        self.assertTrue(TestSubjectResultModel.objects.filter(subject_identifier=subject_identifier, result='POS', result_datetime=value_datetime).count(), 1)
        self.assertTrue(TestSubjectResultModel.objects.filter(subject_identifier=subject_identifier, result='POS', result_datetime__lte=value_datetime).count(), 1)
        print 'history model now returns values from the TestModelResult'
        self.assertEqual(tracker1.get_history(value_datetime).count(), 1)
        print 'attributes are set'
        self.assertEqual(tracker1.get_subject_identifier(), subject_identifier)
        self.assertEqual(tracker1.get_subject_type(), subject_type)
        self.assertEqual(tracker1.get_group_name(), group_name)
        self.assertEqual(tracker1.get_value_datetime(), value_datetime)
        #self.assertEqual(tracker.get_value_datetime(), tracker._get_max_value_datetime())
        self.assertNotEqual(tracker1._get_history_inst().pk, '')

        print 'calling site_lab_tracker.update should not add a new rec to history'
        site_lab_tracker.update_history(test_result_model)
        self.assertEqual(tracker1.get_history(value_datetime).count(), 1)

        print 'test with history, returns current value (POS)'
        self.assertEqual([tracker1._get_history_inst().value, tracker1._get_history_inst().value_datetime, tracker1._get_history_inst().subject_identifier],
                         [unicode(test_result_model.result), test_result_model.result_datetime, unicode(test_result_model.subject_identifier)])
        self.assertEqual('POS', tracker1.get_value(value_datetime))

        print 'change subject_identifier'
        subject_identifier = 'subject_identifier2'
        tracker2 = TestLabTracker(subject_identifier)
        value_datetime = datetime.today() - timedelta(days=5)
        print 'test if no history yet available, returns default value (UNK)'
        self.assertEqual('UNK', tracker2.get_value(value_datetime))
        self.assertEqual(tracker2.get_history(value_datetime=value_datetime).count(), 0)
        print 'attributes are set'
        self.assertEqual(tracker2.get_subject_identifier(), subject_identifier)
        self.assertEqual(tracker2.get_group_name(), group_name)
        self.assertEqual(tracker2.get_value_datetime(), value_datetime)
        self.assertIsNotNone(tracker2._get_history_inst())
        self.assertEqual(tracker2._get_history_inst().pk, '')
        self.assertEqual(tracker2.get_value_datetime(), value_datetime)

        print 'test use of subject_type'

        class TestLabTracker2(LabTracker):
            trackers = [(TestSubjectResultModel, 'result', 'result_datetime', )]
            group_name = 'HIV'
            tracked_test_codes = ('HIV', 'ELISA', 'RELISA')
        print site_lab_tracker._registry
        self.assertRaises(ImproperlyConfigured, site_lab_tracker.register, TestLabTracker2)

        class TestLabTracker3(LabTracker):
            subject_type = 'invalid'
            trackers = [(TestSubjectResultModel, 'result', 'result_datetime', )]
            group_name = 'HIV'
            tracked_test_codes = ('HIV', 'ELISA', 'RELISA')

        self.assertRaises(ImproperlyConfigured, site_lab_tracker.register, TestLabTracker3)

        class TestLabTracker5(LabTracker):
            subject_type = settings.SUBJECT_TYPES[0]
            trackers = [(TestSubjectResultModel, 'result', 'result_datetime', )]
            group_name = 'HIV'
            tracked_test_codes = ('HIV', 'ELISA', 'RELISA')

        self.assertIsNone(site_lab_tracker.register(TestLabTracker5))

        print 'if subject_type and group_name not unique, fails'

        class TestLabTracker6(LabTracker):
            subject_type = settings.SUBJECT_TYPES[0]
            trackers = [(TestSubjectResultModel, 'result', 'result_datetime', )]
            group_name = 'HIV'
            tracked_test_codes = ('HIV', 'ELISA', 'RELISA')
        self.assertRaises(AlreadyRegistered, site_lab_tracker.register, TestLabTracker6)

        site_lab_tracker.unregister(TestLabTracker2)
        site_lab_tracker.unregister(TestLabTracker3)
        site_lab_tracker.unregister(TestLabTracker5)
        site_lab_tracker.unregister(TestLabTracker6)

        print 'site_lab_tracker.autodiscover()'
        site_lab_tracker.register(TestLabTracker)
        site_lab_tracker.autodiscover()
        print 'create registered_subject'
        registered_subject = RegisteredSubjectFactory(subject_identifier=subject_identifier, subject_type='test_subject_type')
        print 'create receive'
        receive = ReceiveFactory(registered_subject=registered_subject)
        print 'create aliquot_condition'
        aliquot_condition = AliquotConditionFactory(short_name='10', name='ok')
        print 'create aliquot'
        aliquot = AliquotFactory(receive=receive, aliquot_condition=aliquot_condition)
        print 'create order'
        order = OrderFactory(aliquot=aliquot)
        print 'create result'
        result = ResultFactory(order=order)
        test_code = TestCodeFactory(code='ELISA')
        print 'create result item with test code ELISA (tracked)'
        result_item1 = ResultItemFactory(result=result, test_code=test_code, subject_type='test_subject_type')
        print 'count=0 for history model for this subject {0} up to {1}'.format(subject_identifier, value_datetime)
        self.assertEqual(tracker2.get_history(value_datetime=value_datetime).count(), 0)
        print 'count=1 for history model for this subject {0} up to {1}'.format(subject_identifier, result_item1.result_item_datetime)
        self.assertEqual(tracker2.get_history(value_datetime=result_item1.result_item_datetime).count(), 1)
        print 'create result item with factory test code (not tracked)'
        result_item2 = ResultItemFactory(result=result, subject_type='test_subject_type')
        print 'count=1 for history model for this subject {0}'.format(subject_identifier)
        self.assertEqual(tracker2.get_history(value_datetime=result_item2.result_item_datetime).count(), 1)
        print 'create another result item with test code ELISA (tracked)'
        result_item3 = ResultItemFactory(result=result, test_code=test_code, result_item_datetime=datetime.today(), subject_type='test_subject_type')
        print 'count=2 for history model for this subject {0}'.format(subject_identifier)
        self.assertEqual(tracker2.get_history(value_datetime=result_item3.result_item_datetime).count(), 2)
        self.assertEqual(result_item3.result_item_value, tracker2.get_value(result_item3.result_item_datetime))
        self.assertEqual(tracker2.get_history_as_string(reference_datetime=result_item3.result_item_datetime), ''.join(sorted([result_item1.result_item_value, result_item3.result_item_value])))

        # test get_current_history / value returns the correct value relative to the value_datetime
        print 'change subject_identifier'
        subject_identifier = 'subject_identifier3'
        tracker3 = TestLabTracker(subject_identifier)
        value_datetime = None
        self.assertRaises(TypeError, tracker3._get_history_inst)
        #tracker3._update_history_for_inst(result_item1, tracker3)

        TestSubjectResultModelFactory()
