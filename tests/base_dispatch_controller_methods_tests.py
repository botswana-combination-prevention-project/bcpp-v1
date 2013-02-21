from datetime import datetime
from django.core.exceptions import ValidationError, ImproperlyConfigured, MultipleObjectsReturned
from django.db import IntegrityError
from django.db.models import get_model
from django.conf import settings
from django.test import TestCase
from bhp_sync.models import Producer
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsentedUuidModel
from bhp_dispatch.classes import BaseDispatch
from bhp_dispatch.exceptions import AlreadyDispatched, DispatchError, DispatchModelError
from bhp_dispatch.models import DispatchContainer


class BaseDispatchControllerMethodsTests(TestCase):

    def setUp(self, dispatch_container_app_label, dispatch_container_model_name, dispatch_container_identifier_attrname, dispatch_container_identifier, dispatch_item_app_label):
        Producer.objects.create(name='test_producer', settings_key='dispatch_destination', is_active=True)
        self.base_controller = BaseDispatch(
            'default',
            'dispatch_destination',
            dispatch_container_app_label,
            dispatch_container_model_name,
            dispatch_container_identifier_attrname,
            dispatch_container_identifier,
            dispatch_item_app_label)

    def test_get_dispatch_instance(self):
        #assert a dispatch instance exists
        self.assertIsInstance(self.base_controller.get_dispatch_container_instance(), DispatchContainer)
        # assert that dispatch instance producer
        self.assertEqual(self.base_controller.get_dispatch_container_instance().producer, self.base_controller.get_producer())
        # assert dispatch instance is_dispatched=True
        self.assertTrue(self.base_controller.get_dispatch_container_instance().is_dispatched)
        # assert values in dispatch_container_instance
        self.assertEquals(self.base_controller.get_dispatch_container_instance().container_identifier, self.base_controller.get_dispatch_container_identifier())
        # get the container user instance
        obj_cls = get_model(
            self.base_controller.get_dispatch_container_instance().container_app_label,
            self.base_controller.get_dispatch_container_instance().container_model_name)
        self.assertIsInstance(
            obj_cls.objects.get(**{self.base_controller.get_dispatch_container_instance().container_identifier_attrname: self.base_controller.get_dispatch_container_instance().container_identifier}),
            obj_cls)
        self.assertEquals(self.base_controller.get_dispatch_container_instance().container_identifier, self.base_controller.get_dispatch_container_identifier())
        #assert container user model now is dispatched on updates
        obj = obj_cls.objects.get(**{self.base_controller.get_dispatch_container_instance().container_identifier_attrname: self.base_controller.get_dispatch_container_instance().container_identifier})
        # assert that user container model identifier attrname is same as one used to init the class
        self.assertEqual(obj.dispatched_as_container_identifier_attr(), self.base_controller.get_dispatch_container_identifier_attrname())
        # assert that user container model is flagged as a container model
        self.assertTrue(obj.is_dispatch_container_model())
        # assert that users container model is flagged as dispatched
        self.assertTrue(obj.is_dispatched)
        #self.assertRaises(AlreadyDispatched, obj.save)

    def test_get_scheduled_models(self):
        # assert that the dispatch item app is set (set in setUp)
        self.assertIsNotNone(self.base_controller.get_dispatch_item_app_label())
        # get the scheduled models
        scheduled_models = self.base_controller.get_scheduled_models()
        # assert that return value is a list
        self.assertIsInstance(scheduled_models, list)
        # assert that some scheduled model classes were returned
        self.assertGreaterEqual(len(scheduled_models), 0)
        # assert that returned list contains classes that are subclassed from BaseConsentedUuidModel
        # ... must be true for all scheduled models in an app.
        for scheduled_model in scheduled_models:
            self.assertTrue(issubclass(scheduled_model, BaseConsentedUuidModel))

    def test_get_membershipform_models(self):
        membershipform_models = self.base_controller.get_membershipform_models()
        self.assertIsInstance(membershipform_models, list)
        for membershipform_model in membershipform_models:
            self.assertTrue(hasattr(membershipform_model, 'registered_subject'))

    def test_set_producer(self):
        # assert there is a contraint on settings_key and is_active
        self.assertRaises(IntegrityError, Producer.objects.create, name='test_producer', settings_key='dispatch_destination', is_active=True)
        # update the current producer to in_active
        current_producer = self.base_controller.get_producer()
        current_producer.is_active = False
        current_producer.save()
        # add a new producer
        new_producer = Producer.objects.create(name='test_producer_2', settings_key='dispatch_destination', is_active=True)
        # call set producer (there is only one active for 'dispatch_destination'
        self.base_controller.set_producer()
        # assert name of producer is now 'test_producer_2'
        self.assertEqual(new_producer.name, self.base_controller.get_producer_name())
        # assert dispatch list is None as there is no dispatch item yet
        self.assertQuerysetEqual(self.base_controller.get_dispatched_items_for_producer(), [])
