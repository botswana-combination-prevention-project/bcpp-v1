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
        self.create_producer(is_active=True)
        self.create_test_item()
        return_controller = ReturnController(self.using_source, self.using_destination)
        dispatch_container = None
        return_controller.return_dispatch_items_for_container(dispatch_container)
        self.create_base_dispatch_controller()
        dispatch_container = self.base_dispatch_controller.get_dispatch_container_instance()
        self.assertIsInstance(dispatch_container, DispatchContainer)
        return_controller.return_dispatch_items_for_container(dispatch_container)
        obj_cls = get_model(
            self.base_dispatch_controller.get_dispatch_container_instance().container_app_label,
            self.base_dispatch_controller.get_dispatch_container_instance().container_model_name)
        obj = obj_cls.objects.get(**{dispatch_container.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_instance().container_identifier})
        self.base_dispatch_controller.dispatch_as_json(obj)
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=True).count(), 1)
        return_controller.return_dispatch_items_for_container(dispatch_container)
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=False).count(), 1)
        self.base_dispatch_controller.dispatch_as_json(obj)
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=True).count(), 1)
        return_controller.return_dispatched_items()
        self.assertEqual(DispatchItem.objects.filter(is_dispatched=False).count(), 2)
