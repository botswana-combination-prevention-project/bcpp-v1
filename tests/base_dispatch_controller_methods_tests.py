from datetime import datetime
from django.db import IntegrityError
from django.db.models import get_model
from django.test import TestCase
from bhp_sync.models import Producer
from bhp_consent.models import BaseConsentedUuidModel
from bhp_dispatch.classes import BaseDispatch, ReturnController, BaseDispatchController
from bhp_dispatch.exceptions import AlreadyDispatched, DispatchError, AlreadyDispatchedContainer
from bhp_dispatch.models import DispatchContainerRegister, TestItem, TestContainer, DispatchItemRegister


class BaseDispatchControllerMethodsTests(TestCase):

    def setUp(self, user_container_app_label=None, user_container_model_name=None, user_container_identifier_attrname=None, user_container_identifier=None, dispatch_item_app_label=None):
        Producer.objects.create(name='test_producer', settings_key='dispatch_destination', is_active=True)
        self.producer = None
        self.outgoing_transaction = None
        self.incoming_transaction = None
        self.using_source = 'default'
        self.using_destination = 'dispatch_destination'
        self.user_container_app_label = user_container_app_label or 'bhp_dispatch'
        self.user_container_model_name = user_container_model_name or 'testcontainer'
        self.user_container_identifier_attrname = user_container_identifier_attrname or 'test_container_identifier'
        self.user_container_identifier = user_container_identifier or 'TEST_IDENTIFIER'
        self.dispatch_item_app_label = 'bhp_dispatch'  # usually something like 'mochudi_subject'
        # create an instance for the container before initiation the class
        self.create_test_container()
        self.base_controller = BaseDispatch(
            'default',
            'dispatch_destination',
            self.user_container_app_label,
            self.user_container_model_name,
            self.user_container_identifier_attrname,
            self.user_container_identifier)

    def create_test_container(self):
        self.test_container = TestContainer.objects.create(test_container_identifier=self.user_container_identifier)

#    def create_test_item(self):
#        self.test_container = TestItem.objects.create(test_container_identifier='TEST_ITEM_IDENTIFIER')

    def test_container_model(self):
        # assert that you cannot use TestItem as a container model
        self.assertRaises(DispatchError, BaseDispatch,
            'default',
            'dispatch_destination',
            self.user_container_app_label,
            'testitem',
            'id',
            '0')

    def test_get_dispatch_container_register_instance(self):
        #assert a dispatch container instance exists
        self.assertIsInstance(self.base_controller.get_dispatch_container_register_instance(), DispatchContainerRegister)
        # assert there is only one
        self.assertEqual(DispatchContainerRegister.objects.all().count(), 1)
        # get dispatch_container_register
        dispatch_container_register = self.base_controller.get_dispatch_container_register_instance()
        # assert that dispatch container instance producer is correct
        self.assertEqual(dispatch_container_register.producer, self.base_controller.get_producer())
        # assert dispatch container instance is_dispatched=True
        self.assertTrue(dispatch_container_register.is_dispatched)
        # assert values used to register user_container in dispatch_container_register_instance
        self.assertEquals(dispatch_container_register.container_identifier, self.base_controller.get_user_container_identifier())
        # get the user container instance, e.g. Household
        obj_cls = get_model(
            self.base_controller.get_dispatch_container_register_instance().container_app_label,
            self.base_controller.get_dispatch_container_register_instance().container_model_name)
        # assert this is TestContainer
        self.assertTrue(issubclass(obj_cls, TestContainer))
        # assert this is TestContainer instance
        self.assertIsInstance(
            obj_cls.objects.get(**{dispatch_container_register.container_identifier_attrname: dispatch_container_register.container_identifier}),
            obj_cls)
        obj = obj_cls.objects.get(**{dispatch_container_register.container_identifier_attrname: dispatch_container_register.container_identifier})
        # assert the user container identifier value in the DispatchContainerRegister is the same as is returned by get_user_container_identifier
        self.assertEquals(dispatch_container_register.container_identifier, self.base_controller.get_user_container_identifier())
        #assert get user container instance using base_controller methods
        obj2 = obj_cls.objects.get(**{self.base_controller.get_user_container_identifier_attrname(): self.base_controller.get_dispatch_container_register_instance().container_identifier})
        self.assertEqual(obj2.pk, obj.pk)
        # assert that user container model method returns identifier attrname that is same as one used to init the class
        self.assertEqual(obj.dispatched_as_container_identifier_attr(), self.base_controller.get_user_container_identifier_attrname())
        # assert is an instance of TestContainer
        self.assertTrue(isinstance(obj, TestContainer))
        # assert is a dispatchable model
        self.assertTrue(obj.is_dispatchable_model())
        # assert that user container model is flagged as a container model
        self.assertTrue(obj.is_dispatch_container_model())
        # assert that users container model is flagged as dispatched as a container (DispatchContainer)
        self.assertTrue(obj.is_dispatched_as_container())
        # assert that users container model is NOT flagged as dispatched as an item (DipatchItem)
        self.assertFalse(obj.is_dispatched_as_item())
        # assert that user container instance is dispatched
        #self.assertTrue(obj.is_dispatched())
        # assert that DispatchContainer exists for this user container model
        self.assertIsInstance(DispatchContainerRegister.objects.get(container_identifier=getattr(obj, dispatch_container_register.container_identifier_attrname)), DispatchContainerRegister)
        # assert that DispatchContainer for this user container model is flagged as is_dispatched
        self.assertTrue(DispatchContainerRegister.objects.get(container_identifier=getattr(obj, dispatch_container_register.container_identifier_attrname)).is_dispatched)
        # assert that DispatchContainer for this user container model return_datetime is not set
        self.assertIsNone(DispatchContainerRegister.objects.get(container_identifier=getattr(obj, dispatch_container_register.container_identifier_attrname)).return_datetime)
        # assert model cannot be saved on default
        self.assertRaises(AlreadyDispatchedContainer, obj.save)
        #print [o for o in DispatchItemRegister.objects.all()]
        #print [o for o in DispatchContainerRegister.objects.all()]

    def test_dispatch(self):
        DispatchContainerRegister.objects.all().delete()
        self.assertEqual(DispatchItemRegister.objects.all().count(), 0)
        base_controller = BaseDispatchController(
            'default',
            'dispatch_destination',
            self.user_container_app_label,
            self.user_container_model_name,
            self.user_container_identifier_attrname,
            self.user_container_identifier,
            'bhp_dispatch')
        # get dispatch_container_register
        dispatch_container_register = base_controller.get_dispatch_container_register_instance()
        # get the user container instance, e.g. Household
        user_container_cls = get_model(
            base_controller.get_dispatch_container_register_instance().container_app_label,
            base_controller.get_dispatch_container_register_instance().container_model_name)
        # assert this is TestContainer
        self.assertTrue(issubclass(user_container_cls, TestContainer))
        # assert this is TestContainer instance
        self.assertIsInstance(
            user_container_cls.objects.get(**{dispatch_container_register.container_identifier_attrname: dispatch_container_register.container_identifier}),
            user_container_cls)
        user_container = user_container_cls.objects.get(**{dispatch_container_register.container_identifier_attrname: dispatch_container_register.container_identifier})
        #dispatch as json
        base_controller.dispatch_user_container_as_json(user_container)
        self.assertEqual(DispatchItemRegister.objects.all().count(), 1)
        self.assertEquals(DispatchItemRegister.objects.using(self.using_source).filter(dispatch_container_register=dispatch_container_register).count(), 1)
        #print dispatch_container_register.id
        #print dispatch_container_register
        #print [o for o in DispatchItemRegister.objects.all()]
        #print DispatchItemRegister.objects.get().__dict__
        # update the dispatch_container_register instance as returned
        return_controller = ReturnController(self.using_source, self.using_destination)
        return_controller.return_dispatched_items(user_container)
        # assert that model method also indicates that the instance is NOT dispatched
        self.assertFalse(user_container.is_dispatched_as_container())
        self.assertFalse(user_container.is_dispatched_as_item())

        #print [o for o in DispatchItemRegister.objects.all()]
        # assert the model saves without an exception
        self.assertIsNone(user_container.save())
        DispatchContainerRegister.objects.all().delete()

    def test_set_producer(self):
        # assert there is a contraint on settings_key and is_active
        self.assertRaises(IntegrityError, Producer.objects.create, name='test_producer', settings_key='dispatch_destination', is_active=True)
        base_controller = BaseDispatchController(
            'default',
            'dispatch_destination',
            self.user_container_app_label,
            self.user_container_model_name,
            self.user_container_identifier_attrname,
            self.user_container_identifier,
            'bhp_dispatch')
        # update the current producer to in_active
        current_producer = self.base_controller.get_producer()
        current_producer.is_active = False
        current_producer.save()
        # add a new producer
        new_producer = Producer.objects.create(name='test_producer_2', settings_key='dispatch_destination', is_active=True)
        # call set producer (there is only one active for 'dispatch_destination'
        base_controller.set_producer()
        # assert name of producer is now 'test_producer_2'
        self.assertEqual(new_producer.name, self.base_controller.get_producer_name())
        # assert dispatch list is None as there is no dispatch item yet
        self.assertQuerysetEqual(base_controller.get_dispatched_items_for_producer(), [])


