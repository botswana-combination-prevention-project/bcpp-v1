from django.db.models import get_model
from bhp_sync.exceptions import PendingTransactionError
from bhp_sync.models import OutgoingTransaction
from bhp_dispatch.exceptions import AlreadyDispatched, AlreadyDispatchedContainer, AlreadyDispatchedItem
from bhp_dispatch.models import TestItem, DispatchItem, DispatchContainer
from bhp_dispatch.classes import ReturnController
from base_controller_tests import BaseControllerTests


class ReturnControllerMethodsTests(BaseControllerTests):

    def test_return_controller(self):
        TestItem.objects.using(self.using_destination).all().delete()
        TestItem.objects.all().delete()
        self.create_producer(is_active=True)
        self.create_test_item()
        self.assertEqual(DispatchItem.objects.all().count(), 0)
        self.assertEquals(TestItem.objects.using(self.using_destination).all().count(), 0)
        return_controller = ReturnController(self.using_source, self.using_destination)
        self.assertEqual(DispatchItem.objects.all().count(), 0)
        dispatch_container = None
        return_controller.return_dispatched_items_for_container(dispatch_container)
        # assert nothing was dispatched to the producer
        self.assertEquals(TestItem.objects.using(return_controller.get_using_destination()).all().count(), 0)
        self.assertEqual(DispatchItem.objects.all().count(), 0)
        self.create_base_dispatch_controller()
        obj_cls = get_model(
            self.base_dispatch_controller.get_dispatch_container_instance().container_app_label,
            self.base_dispatch_controller.get_dispatch_container_instance().container_model_name)
        dispatch_container = self.base_dispatch_controller.get_dispatch_container_instance()
        self.assertIsInstance(dispatch_container, DispatchContainer)
        # assert that nothing was dispatched to the producer yet
        self.assertEquals(obj_cls.objects.using(self.base_dispatch_controller.get_using_destination()).filter(**{dispatch_container.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_instance().container_identifier}).count(), 0)
        # assert no dispatch items yet
        self.assertEqual(DispatchItem.objects.all().count(), 0)
        return_controller.return_dispatched_items_for_container(dispatch_container)
        self.assertEqual(DispatchItem.objects.all().count(), 0)
        obj = obj_cls.objects.get(**{dispatch_container.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_instance().container_identifier})
        self.assertEquals(TestItem.objects.using(return_controller.get_using_destination()).all().count(), 0)
        # dispatch the test_item
        self.base_dispatch_controller.dispatch_as_json(obj)
        # assert dispatch item created
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=True).count(), 1)
        # return the test item
        return_controller.return_dispatched_items_for_container(dispatch_container)
        # assert the dispatch item is flagged as is_dispatched = false
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=False, return_datetime__isnull=False).count(), 1)
        # dispatch the test item again
        self.base_dispatch_controller.dispatch_as_json(obj)
        # assert dispatch item is updated
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=True, return_datetime__isnull=True).count(), 1)
        # assert that only one instance was ever created on the producer
        self.assertEqual(obj.__class__.objects.using(return_controller.get_using_destination()).all().count(), 1)
        # try to change the item and confirm no DispatchError raised
        obj.comment = 'TEST_COMMENT'
        self.assertIsNone(obj.save(using=return_controller.get_using_destination()))
        # delete the item on the producer
        obj.__class__.objects.using(return_controller.get_using_destination()).all().delete()
        # return items for producer
        return_controller.return_dispatched_items()
        # assert no dispatched DispatchItems
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=False).count(), 1)
        # chane the instance of TestItem
        obj.comment = 'TEST_COMMENT'
        # assert saving the TestItem, on the source, will fail because this is a container model as well!
        self.assertRaises(AlreadyDispatchedContainer, obj.save)
        # assert saving on destination will NOT raise an exception
        self.assertIsNone(obj.save(using=return_controller.get_using_destination()))
        # return the dispatch container
        return_controller.return_dispatched_container(dispatch_container)
        self.assertFalse(dispatch_container.is_dispatched)
        # try to change the TestItem again
        obj.comment = 'TEST_COMMENT2'
        # assert saving on source will NOT raise any AlreadyDispatched errors
        self.assertIsNone(obj.save())
        # flip the dispatch_container back to dispatched
        #dispatch_container.is_dispatched = True
        #dispatch_container.save()
        # dispatch the TestItem to the producer, again
        #TODO: note this is being dispatched without a container??
        self.base_dispatch_controller.dispatch_as_json(obj)
        # assert changed comment field is correct on the producer
        self.assertEqual(obj.__class__.objects.using(return_controller.get_using_destination()).get(test_item_identifier=obj.test_item_identifier).comment, 'TEST_COMMENT2')
        # edit the TestItem on producer so that a transaction is created
        obj.__class__.objects.using(return_controller.get_using_destination()).get(test_item_identifier=obj.test_item_identifier).comment = 'CHANGED TEST COMMENT'
        # if instance is saved on source, raises an exception (remember, no dispatch container)
        self.assertRaises(AlreadyDispatchedItem, obj.save)
        # if instance is saved on producer does not raise an exception
        self.assertIsNone(obj.save(using=return_controller.get_using_destination()))
        # assert an Outgoing sync transaction exists on the producer
        self.assertEqual(OutgoingTransaction.objects.using(return_controller.get_using_destination()).all().count(), 1)
        # create some sync transactions on the source
        #self.create_sync_transactions()
        # assert that return_dispatched_items will fail
        self.assertRaises(PendingTransactionError, return_controller.return_dispatched_items)
        # TODO: confirm that transactions can be synced while is_dispatched=True
