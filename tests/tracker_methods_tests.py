from datetime import datetime, timedelta
from django.test import TestCase
from django.db.models import signals
from bhp_variables.tests.factories import StudySpecificFactory
from bhp_lab_tracker.classes import LabTracker, site_lab_tracker
from lab_clinic_api.models import ResultItem
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_lab_tracker.models import TestResultModel, HistoryModel, tracker_on_post_save
from lab_clinic_api.tests.factories import ResultItemFactory, AliquotConditionFactory, AliquotFactory, OrderFactory, ReceiveFactory, ResultFactory, TestCodeFactory


class TrackerMethodsTests(TestCase):

    def test_init(self):
        StudySpecificFactory()
        tracker = LabTracker()
        self.assertEqual(tracker.trackers, None)
        # get models, sets the model
        self.assertTrue(isinstance(tracker.get_trackers(), list))
        # at least result item is included
        self.assertEquals(len(tracker.get_trackers()), 1)
        self.assertEquals(tracker.get_trackers()[0][0], ResultItem)

        class TestLabTracker(LabTracker):
            trackers = [(TestResultModel, 'result', 'result_datetime', )]
            group_name = 'HIV'
            resultitem_test_code = ('HIV', 'ELISA', 'RELISA')
            tracker_test_code = 'HIV'

        tracker = TestLabTracker()
        self.assertNotEqual(tracker.trackers, None)
        # get models, sets the model
        self.assertTrue(isinstance(tracker.get_trackers(), list))
        # at least result item is included
        self.assertEquals(len(tracker.get_trackers()), 2)
        trackers = [tracker_tpl[0] for tracker_tpl in tracker.get_trackers()]
        self.assertTrue(ResultItem in trackers)
        self.assertTrue(TestResultModel in trackers)
        subject_identifier = 'subject_identifier1'
        value_datetime = datetime.today() - timedelta(days=5)
        group_name = 'HIV'

        print 'test if no history yet available, returns default value (UNK)'
        self.assertEqual(tracker.get_history(subject_identifier, value_datetime).count(), 0)
        self.assertEqual('UNK', tracker.get_current_value(subject_identifier, value_datetime))
        self.assertTrue(isinstance(tracker._get_current_history_inst(), HistoryModel))
        self.assertTrue(tracker._get_current_history_inst().subject_identifier, subject_identifier)
        self.assertTrue(tracker._get_current_history_inst().value_datetime, value_datetime)
        self.assertTrue(tracker._get_current_history_inst().value, 'UNK')
        self.assertTrue(tracker._get_current_history_inst().pk == '')

        print 'add a TestModelResult with a POS result value to the tracker model'
        self.assertEqual(tracker.get_history(subject_identifier, value_datetime).count(), 0)
        test_result_model = TestResultModel.objects.create(subject_identifier=subject_identifier, result='POS', result_datetime=value_datetime)
        self.assertTrue(TestResultModel.objects.filter(subject_identifier=subject_identifier, result='POS', result_datetime=value_datetime).count(), 1)
        self.assertTrue(TestResultModel.objects.filter(subject_identifier=subject_identifier, result='POS', result_datetime__lte=value_datetime).count(), 1)
        print 'history model now returns values from the TestModelResult'
        self.assertEqual(tracker.get_history(subject_identifier, value_datetime).count(), 1)
        print 'attributes are set'
        self.assertEqual(tracker.get_subject_identifier(), subject_identifier)
        self.assertEqual(tracker.get_group_name(), group_name)
        self.assertEqual(tracker.get_value_datetime(), value_datetime)
        #self.assertEqual(tracker.get_value_datetime(), tracker._get_max_value_datetime())
        self.assertNotEqual(tracker._get_current_history_inst().pk, '')

        print 'calling site_lab_tracker.update should not add a new rec to history'
        site_lab_tracker.update(test_result_model)
        self.assertEqual(tracker.get_history(subject_identifier, value_datetime).count(), 1)

        print 'test with history, returns current value (POS)'
        self.assertEqual([tracker._get_current_history_inst().value, tracker._get_current_history_inst().value_datetime, tracker._get_current_history_inst().subject_identifier],
                         [unicode(test_result_model.result), test_result_model.result_datetime, unicode(test_result_model.subject_identifier)])
        self.assertEqual('POS', tracker.get_current_value(subject_identifier, value_datetime))

        print 'change subject_identifier'
        subject_identifier = 'subject_identifier2'
        value_datetime = None
        print 'test if no history yet available, returns default value (UNK)'
        self.assertEqual(tracker.get_history(subject_identifier, None).count(), 0)
        print 'attributes are set'
        self.assertEqual(tracker.get_subject_identifier(), subject_identifier)
        self.assertEqual(tracker.get_group_name(), group_name)
        self.assertEqual(tracker.get_value_datetime(), value_datetime)
        self.assertEqual(tracker._get_current_history_inst().pk, '')
        self.assertEqual(tracker.get_value_datetime(), value_datetime)

        print 'site_lab_tracker.autodiscover()'
        site_lab_tracker.autodiscover()
        print 'create registered_subject'
        registered_subject = RegisteredSubjectFactory(subject_identifier=subject_identifier)
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
        ResultItemFactory(result=result, test_code=test_code)
        print 'count=1 for history model for this subject {0}'.format(subject_identifier)
        self.assertEqual(tracker.get_history(subject_identifier, None).count(), 1)
        print 'create result item with factory test code (not tracked)'
        ResultItemFactory(result=result)
        print 'count=1 for history model for this subject {0}'.format(subject_identifier)
        self.assertEqual(tracker.get_history(subject_identifier, None).count(), 1)
        print 'create another result item with test code ELISA (tracked)'
        result_item = ResultItemFactory(result=result, test_code=test_code, result_item_datetime=datetime.today())
        print 'count=2 for history model for this subject {0}'.format(subject_identifier)
        self.assertEqual(tracker.get_history(subject_identifier, None).count(), 2)
        self.assertEqual(result_item.result_item_value, tracker.get_current_value(subject_identifier, result_item.result_item_datetime))
