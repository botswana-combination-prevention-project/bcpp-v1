from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test import TestCase
from django.db.models import get_model
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsentedUuidModel
from bhp_sync.models import Producer, OutgoingTransaction, IncomingTransaction
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.classes import Base, BaseDispatchController
from bhp_dispatch.exceptions import DispatchError, AlreadyDispatched
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
        return_controller.return_dispatch_items_for_container(dispatch_container)
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
        return_controller.return_dispatch_items_for_container(dispatch_container)
        self.assertEqual(DispatchItem.objects.all().count(), 0)
        obj = obj_cls.objects.get(**{dispatch_container.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_instance().container_identifier})
        self.assertEquals(TestItem.objects.using(return_controller.get_using_destination()).all().count(), 0)
        # dispatch the test_item
        self.base_dispatch_controller.dispatch_as_json(obj)
        # assert dispatch item created
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=True).count(), 1)
        # return the test item
        return_controller.return_dispatch_items_for_container(dispatch_container)
        # assert the dispatch item is flagged as is_dispatched = false
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=False, return_datetime__isnull=False).count(), 1)
        # dispatch the test item again
        self.base_dispatch_controller.dispatch_as_json(obj)
        # assert dispatch item is updated
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=True, return_datetime__isnull=True).count(), 1)
        # assert that only one instance was ever created on the producer
        self.assertEqual(obj.__class__.objects.using(return_controller.get_using_destination()).all().count(), 1)
        # delete the item on the producer
        obj.__class__.objects.using(return_controller.get_using_destination()).all().delete()
        # return items for producer
        return_controller.return_dispatched_items()
        # what happens now??
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=False).count(), 1)
        obj.comment = 'TEST_COMMENT'
        obj.save()
        self.base_dispatch_controller.dispatch_as_json(obj)
        self.assertEqual(obj.__class__.objects.using(return_controller.get_using_destination()).get(item_identifier=obj.item_identifier).comment, 'TEST_COMMENT')
