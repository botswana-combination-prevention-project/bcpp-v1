from django.db.models import get_model
from bhp_sync.exceptions import PendingTransactionError
from bhp_sync.models import OutgoingTransaction
from bhp_dispatch.exceptions import AlreadyDispatched, AlreadyDispatchedContainer, AlreadyDispatchedItem, DispatchError, AlreadyReturnedController, DispatchContainerError
from bhp_dispatch.models import TestItem, DispatchItemRegister, DispatchContainerRegister, TestContainer
from bhp_dispatch.classes import ReturnController
from base_controller_tests import BaseControllerTests


class ReturnControllerMethodsTests(BaseControllerTests):

    def test_return_controller(self):
        TestItem.objects.using(self.using_destination).all().delete()
        TestItem.objects.all().delete()
        self.create_producer(is_active=True)
        self.create_test_item()
        # assert not instances registered to DispatchItemRegister
        self.assertEqual(DispatchItemRegister.objects.all().count(), 0)
        # assert no TestItem on destination
        self.assertEquals(TestItem.objects.using(self.using_destination).all().count(), 0)
        # get a return controller
        return_controller = ReturnController(self.using_source, self.using_destination)
        # assert still not instances registered to DispatchItemRegister
        self.assertEqual(DispatchItemRegister.objects.all().count(), 0)
        dispatch_container_register = None
        return_controller.return_dispatched_items(dispatch_container_register)
        # assert nothing was dispatched to the producer
        self.assertEquals(TestItem.objects.using(return_controller.get_using_destination()).all().count(), 0)
        self.assertEqual(DispatchItemRegister.objects.all().count(), 0)
        self.create_base_dispatch_controller()
        obj_cls = get_model(
            self.base_dispatch_controller.get_dispatch_container_register_instance().container_app_label,
            self.base_dispatch_controller.get_dispatch_container_register_instance().container_model_name)
        dispatch_container_register = self.base_dispatch_controller.get_dispatch_container_register_instance()
        self.assertIsInstance(dispatch_container_register, DispatchContainerRegister)
        # assert that nothing was dispatched to the producer yet
        self.assertEquals(obj_cls.objects.using(self.base_dispatch_controller.get_using_destination()).filter(**{dispatch_container_register.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_register_instance().container_identifier}).count(), 0)
        # assert no dispatch items yet
        self.assertEqual(DispatchItemRegister.objects.all().count(), 0)
        return_controller.return_dispatched_items(dispatch_container_register)
        self.assertEqual(DispatchItemRegister.objects.all().count(), 0)
        obj = obj_cls.objects.get(**{dispatch_container_register.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_register_instance().container_identifier})
        self.assertEquals(TestItem.objects.using(return_controller.get_using_destination()).all().count(), 0)

        # get a new controller
        self.base_dispatch_controller = None
        self.create_base_dispatch_controller()
        # assert raises DispatchError as you cannot use dispatch_container_register as a user_container
        self.assertRaises(DispatchError, self.base_dispatch_controller.dispatch_user_items_as_json, obj, dispatch_container_register)
        if not self.test_container:
            self.create_test_container()
        # assert Raises dispatch error becuase user item and container are same class
        self.assertRaises(DispatchError, self.base_dispatch_controller.dispatch_user_items_as_json, obj, self.test_container)
        TestContainer.objects.all().delete()
        self.create_test_container()
        # assert raises error because user item in None
        self.assertRaises(DispatchError, self.base_dispatch_controller.dispatch_user_items_as_json, None, self.test_container)
        self.create_test_item()
        self.base_dispatch_controller.dispatch_user_items_as_json(self.test_item, self.test_container)
        # assert dispatch item created
        self.assertEqual(DispatchItemRegister.objects.filter(is_dispatched=True).count(), 1)
        # assert error since the controller was initialized before the test_container instance was created
        self.assertRaises(DispatchContainerError, return_controller.return_dispatched_items, self.test_container)

        # get a new controller
        self.base_dispatch_controller = None
        self.create_base_dispatch_controller()
        obj = self.test_item
        # assert error when dispatch the test item again becuase it was never returned from the last controller
        self.assertRaises(AlreadyDispatchedItem, self.base_dispatch_controller.dispatch_user_items_as_json, obj, self.test_container)
        # assert dispatch item is updated
        self.assertEqual(DispatchItemRegister.objects.filter(is_dispatched=True, return_datetime__isnull=True).count(), 1)
        # assert that only one instance was ever created on the producer
        self.assertEqual(obj.__class__.objects.using(return_controller.get_using_destination()).all().count(), 1)
        # try to change the item and confirm no DispatchError raised
        obj.comment = 'TEST_COMMENT'
        self.assertIsNone(obj.save(using=return_controller.get_using_destination()))
        self.assertRaises(AlreadyDispatchedItem, obj.save)
        # delete the item on the producer
        #obj.__class__.objects.using(return_controller.get_using_destination()).all().delete()
        # return items for producer
        return_controller.return_dispatched_items()
        # assert no dispatched DispatchItemRegisters
        self.assertEqual(DispatchItemRegister.objects.filter(is_dispatched=False).count(), 2)
        self.assertFalse(dispatch_container_register.is_dispatched)
        # try to change the TestItem again
        obj.comment = 'TEST_COMMENT2'
        # assert saving on source will NOT raise any AlreadyDispatched errors
        self.assertIsNone(obj.save())
        # dispatch the TestItem to the producer, again
        #TODO: note this is being dispatched without a container??
        self.base_dispatch_controller.dispatch_user_items_as_json(obj, dispatch_container_register)
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
