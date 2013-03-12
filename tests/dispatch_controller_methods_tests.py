from datetime import datetime
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.test import TestCase
from django.db.models import get_model
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsentedUuidModel
from bhp_sync.models import Producer, OutgoingTransaction, IncomingTransaction
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.classes import Base, BaseDispatchController, ReturnController
from bhp_dispatch.exceptions import DispatchError, AlreadyDispatched, AlreadyDispatchedItem, AlreadyDispatchedContainer, AlreadyReturnedController
from bhp_dispatch.models import TestItem, DispatchItemRegister, DispatchContainerRegister, TestContainer
from base_controller_tests import BaseControllerTests


class DispatchControllerMethodsTests(BaseControllerTests):

    #fixtures = ['test_configuration.json']

#    def setUp(self):
#        super(DispatchControllerMethodsTests, self).setUp()

#    def create_test_item(self):
#        self.test_item = TestItem.objects.create(test_item_identifier=self.dispatch_container_identifier)
#
#    def create_producer(self, is_active=False):
#        # add a in_active producer
#        self.producer = Producer.objects.create(name='test_producer', settings_key=self.using_destination, is_active=is_active)

    def test_base_methods(self):
        # Base tests
        self.assertTrue('DEVICE_ID' in dir(settings), 'Settings attribute DEVICE_ID not found')
        # raise source and destination cannot be the same
        self.assertRaises(DispatchError, Base, self.using_source, self.using_source)
        # source must be either server or default
        self.assertRaises(DispatchError, Base, 'not_default', self.using_source)
        # no producer for destination
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination)
        if not self.producer:
            self.create_producer()
        self.assertIsInstance(self.producer, Producer)
        self.assertEqual(self.producer.settings_key, self.using_destination)
        # no active producer for destination
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination)
        # activate producer
        self.producer.is_active = True
        self.producer.save()
        # Base instance creates OK
        base = Base(self.using_source, self.using_destination)
        self.assertIsInstance(base, Base)
        # confirm producer instance is as expected
        self.assertEqual(base.get_producer().settings_key, self.producer.settings_key)
        # DATABASE keys check works
        self.assertRaises(ImproperlyConfigured, Base(self.using_source, self.using_destination).is_valid_using, 'xdefault', 'source')
        # ...
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination, server_device_id=None)
        # id source is default, must be server = 99
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination, server_device_id='22')
        #TODO: improve use of DEVICE_ID and server_device_id
        Producer.objects.all().delete()

    def test_base_dispatch_methods(self):
        if not self.producer:
            self.create_producer(True)
        # add outgoing transactions and check is properly detects pending transactions before dispatching
        self.create_sync_transactions()
        # create an instance for the user container model
        # ... try get_model with self attributes first
        self.assertIsNotNone(get_model(self.dispatch_container_app_label, self.dispatch_container_model_name))
        self.create_test_container()
        # assert test_item instance created
        self.assertIsInstance(self.test_container, TestContainer)
        self.assertEqual(TestContainer.objects.filter(**{self.dispatch_container_identifier_attrname: self.dispatch_container_identifier}).count(), 1)
        self.assertEqual(getattr(TestContainer.objects.get(**{self.dispatch_container_identifier_attrname: self.dispatch_container_identifier}), self.dispatch_container_identifier_attrname), self.dispatch_container_identifier)
        # assert Trasactions created
        #print [o.tx_name for o in OutgoingTransaction.objects.using(self.using_destination).filter(is_consumed=False)]
        self.assertEquals(OutgoingTransaction.objects.using(self.using_destination).filter(is_consumed=False).count(), 1)
        self.base_dispatch_controller = None
        # create base controller instance
        self.create_base_dispatch_controller()
        # assert there ARE outgoing transactions on dispatch_destination
        self.assertTrue(self.base_dispatch_controller.has_outgoing_transactions())
        #print [o for o in OutgoingTransaction.objects.using('dispatch_destination').filter(is_consumed=False)]
        # assert there ARE incoming transactions on default
        self.assertTrue(self.base_dispatch_controller.has_incoming_transactions())
        self.assertTrue(self.base_dispatch_controller.has_incoming_transactions(RegisteredSubject))
        # assert that Base().dispatch_model_as_json must have a model passed to it
        # self.assertRaises(DispatchModelError, base_dispatch_controller.dispatch_as_json, None)
        # assert that a dispatch_model_as_json fails due to pending transactions
        self.assertRaises(PendingTransactionError, self.base_dispatch_controller.dispatch_user_items_as_json, RegisteredSubject)
        # consume outgoing transaction
        OutgoingTransaction.objects.using(self.using_destination).all().update(is_consumed=True)
        self.assertFalse(self.base_dispatch_controller.has_outgoing_transactions())
        # assert that a dispatch_model_as_json still fails due to pending incoming transactions
        self.assertRaises(PendingTransactionError, self.base_dispatch_controller.dispatch_user_items_as_json, RegisteredSubject)
        # confirm no pending outgoing
        self.assertFalse(self.base_dispatch_controller.has_outgoing_transactions())
        # consume incoming transaction
        IncomingTransaction.objects.all().update(is_consumed=True)
        self.assertFalse(self.base_dispatch_controller.has_incoming_transactions())
        # assert there are no pending incoming transactions
        self.assertFalse(self.base_dispatch_controller.has_incoming_transactions(RegisteredSubject))
        # assert there are no pending transactions
        self.assertFalse(self.base_dispatch_controller.has_pending_transactions(RegisteredSubject))

        # create a few registsred subject instances on default
        subject_identifiers = ['subjectA', 'subjectB', 'subjectC']
        for subject_identifier in subject_identifiers:
            RegisteredSubject.objects.using(self.using_source).create(subject_identifier=subject_identifier)
        # assert that outgoing transactions were created (2 for each -- one for model, one for audit)
        #print [o.tx_name for o in OutgoingTransaction.objects.using(self.using_destination).filter(is_consumed=False)]
        self.assertEquals(OutgoingTransaction.objects.using(self.using_source).filter(is_consumed=False).count(), 8)
        #print [rs for rs in RegisteredSubject.objects.all().order_by('id')]
        rs_pks = [rs.pk for rs in RegisteredSubject.objects.all().order_by('id')]
        # assert dispatch_model_as_json accepts RegisteredSubject as a model class
        self.assertEqual(self.base_dispatch_controller.dispatch_model_as_json(RegisteredSubject), None)
        # assert dispatch_as_json does not create any sync transactions
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 8)
        # assert that RegisteredSubject instance is already dispatched
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifiers[0])
        self.assertRaises(AlreadyDispatchedItem, registered_subject.save)
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 8)
        # get a return controller
        return_controller = ReturnController(self.using_source, self.using_destination)
        self.assertTrue(return_controller.return_dispatched_items(RegisteredSubject.objects.filter(subject_identifier__in=subject_identifiers)))
        # assert default can save RegisteredSubject (no longer dispatched)
        self.assertIsNone(registered_subject.save())
        # assert returning items does not create transactions
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 8)
        # assert RegisteredSubject instances were dispatched
        # ... by subject_identifier
        self.assertEqual([rs.subject_identifier for rs in RegisteredSubject.objects.using(self.using_destination).all().order_by('subject_identifier')], subject_identifiers)
        # .. by pk
        self.assertEqual([rs.pk for rs in RegisteredSubject.objects.using(self.using_destination).all().order_by('id')], rs_pks)
        # confirm no transactions were created that concern this producer
        self.assertFalse(self.base_dispatch_controller.has_pending_transactions(RegisteredSubject))
        # assert that serialize on save signal was disconnected and did not create outgoing transactions
        # on source while dispatching_model_to_json
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
        # modify a registered subject on the source to create a transaction on the source
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifiers[0])
        registered_subject.registration_status = 'CONSENTED'
        registered_subject.save()
        # assert transactions were created by modifying registered_subject
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 8)
        # assert that the transaction is not from the producer
        self.assertFalse(self.base_dispatch_controller.has_pending_transactions(RegisteredSubject))
        # modify a registered subject on the destination to create a transaction on the destination
        registered_subject = RegisteredSubject.objects.using(self.using_destination).get(subject_identifier=subject_identifiers[0])
        registered_subject.registration_status = 'CONSENTED'
        registered_subject.save(using=self.using_destination)
        # assert transactions were created by modifying registered_subject
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 9)
        RegisteredSubject.objects.all().delete()
        RegisteredSubject.objects.using(self.using_destination).all().delete()
        #DispatchContainerRegister.objects.all().delete()

#    def test_get_scheduled_models(self):
#        self.create_producer(True)
#        self.create_test_item()
#        # create base controller instance
#        self.create_base_dispatch_controller()
#        # assert that the dispatch item app is set (set in setUp)
#        #self.assertIsNotNone(self.base_dispatch_controller.get_dispatch_item_app_label())
#        # get the scheduled models
#        scheduled_models = self.base_dispatch_controller.get_scheduled_models('bhp_consent')
#        # assert that return value is a list
#        self.assertIsInstance(scheduled_models, list)
#        # assert that some scheduled model classes were returned
#        self.assertGreaterEqual(len(scheduled_models), 0)
#        # assert that returned list contains classes that are subclassed from BaseConsentedUuidModel
#        # ... must be true for all scheduled models in an app.
#        for scheduled_model in scheduled_models:
#            self.assertTrue(issubclass(scheduled_model, BaseConsentedUuidModel))

    def test_get_membershipform_models(self):
        self.create_producer(True)
        self.create_test_container()
        self.create_test_item()
        # create base controller instance
        self.create_base_dispatch_controller()
        membershipform_models = self.base_dispatch_controller.get_membershipform_models()
        self.assertIsInstance(membershipform_models, list)
        for membershipform_model in membershipform_models:
            self.assertTrue(hasattr(membershipform_model, 'registered_subject'))

    def test_dispatch_item_within_container(self):
        """Tests dispatching a test container and or a test item and verifies the model method is_dispatched behaves as expected."""
        TestContainer.objects.all().delete()
        TestContainer.objects.using(self.using_destination).all().delete()
        TestItem.objects.all().delete()
        TestItem.objects.using(self.using_destination).all().delete()
        self.create_producer(True)
        # create a test container model e.g. Household
        self.create_test_container()
        # assert that it is not dispatched
        self.assertFalse(self.test_container.is_dispatched_as_container())
        self.assertFalse(self.test_container.is_dispatched_as_item())
        # create a test item for the container
        self.create_test_item()
        # assert it is not dispatched
        self.assertFalse(self.test_item.is_dispatched_as_container())
        self.assertFalse(self.test_item.is_dispatched_as_item())
        # get a dispatch controller
        self.create_base_dispatch_controller()
        self.assertEquals(DispatchContainerRegister.objects.all().count(), 1)
        pk = DispatchContainerRegister.objects.all()[0].pk
        obj_id = id(self.base_dispatch_controller)
        # assert user container is dispatched as a container but not an item
        self.assertTrue(self.test_container.is_dispatched_as_container())
        self.assertFalse(self.test_container.is_dispatched_as_item())
        # assert a new controller does not create a new DispatchContainerRegister for the same user container
        self.create_base_dispatch_controller()
        # ...still just one
        self.assertEquals(DispatchContainerRegister.objects.all().count(), 1)
        # assert this is still the same DispatchContainerRegister as before
        self.assertEqual(pk, DispatchContainerRegister.objects.all()[0].pk)
        # ... but from a new instance of the controller
        self.assertNotEqual(obj_id, id(self.base_dispatch_controller))
        # dispatch the test_container pnly
        self.base_dispatch_controller.dispatch_user_container_as_json(self.test_container)
        # assert it is now dispatched both as a container and item
        self.assertTrue(self.test_container.is_dispatched_as_container())
        self.assertTrue(self.test_container.is_dispatched_as_item())
        # assert that the TestItem is now evaluated as dispatched only because it's container is dispatched
        self.assertTrue(self.test_item.is_dispatched_as_item())
        self.assertFalse(self.test_item.is_dispatched_as_container())
        # assert only one DispatchItemRegister exists
        self.assertEqual(DispatchItemRegister.objects.all().count(), 1)
        # ... and that it belongs to the user container (TestContainer)
        self.assertEqual(DispatchItemRegister.objects.filter(item_pk=self.test_container.pk).count(), 1)
        # assert that trying to dispatch the user container again fails
        self.assertRaises(AlreadyDispatchedItem, self.base_dispatch_controller.dispatch_user_container_as_json, self.test_container)
        # get a return controller
        return_controller = ReturnController(self.using_source, self.using_destination)
        # return the dispatched items
        return_controller.return_dispatched_items()
        # assert that container is no longer dispatched
        self.assertFalse(self.test_container.is_dispatched_as_container())
        self.assertFalse(self.test_container.is_dispatched_as_item())
        # assert that the DispatchContainerRegister is no longer dispatched
        self.assertFalse(DispatchContainerRegister.objects.get(pk=pk).is_dispatched)
        # assert that the test item is not dispatched (since the container is no longer dispatched)
        self.assertFalse(self.test_item.is_dispatched_as_item())
        # assert that base_dispatch_controller can no longer be used for dispatch, since the DispatchContainerRegister is returned
        self.assertRaises(AlreadyReturnedController, self.base_dispatch_controller.dispatch_user_items_as_json, [self.test_item])
        # create a new controller
        self.base_dispatch_controller = None
        self.create_base_dispatch_controller()
        # assert a new DispatchContainerRegister was created
        self.assertEquals(DispatchContainerRegister.objects.all().count(), 2)
        # dispatch the user container
        self.base_dispatch_controller.dispatch_user_container_as_json(self.test_container)
        # assert test_container is dispatched
        self.assertTrue(self.test_container.is_dispatched_as_container())
        # assert the test item is dispatched
        self.assertTrue(self.test_item.is_dispatched_as_item())
        # return dispatched items
        return_controller.return_dispatched_items()
        # re-assert nothing is dispatched
        self.assertFalse(self.test_container.is_dispatched_as_container())
        self.assertFalse(self.test_item.is_dispatched_as_item())

    def test_models(self):
        self.create_test_container()
        self.assertRegexpMatches(str(self.test_container.pk), r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        self.create_test_item()
        self.assertRegexpMatches(str(self.test_item.pk), r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')

    def test_dispatch_item_and_container(self):
        TestContainer.objects.all().delete()
        TestContainer.objects.using(self.using_destination).all().delete()
        TestItem.objects.all().delete()
        TestItem.objects.using(self.using_destination).all().delete()
        if not self.producer:
            self.create_producer(True)
        self.create_test_item()
        # create base controller instance
        self.base_dispatch_controller = None
        # attempt to create instance using TestItem instead of TestContainer
        # assert raise error as TestItem is not a container model
        self.assertRaises(DispatchError, self.create_base_dispatch_controller, 'testitem')
        # create a new dispatch controller
        self.base_dispatch_controller = None
        self.create_base_dispatch_controller()
        # get the DispatchContanier instance
        dispatch_container_register = self.base_dispatch_controller.get_dispatch_container_register_instance()
        self.assertIsInstance(dispatch_container_register, DispatchContainerRegister)
        # get the model that is being used as a container using information from DispatchContainerRegister
        obj_cls = get_model(
            self.base_dispatch_controller.get_dispatch_container_register_instance().container_app_label,
            self.base_dispatch_controller.get_dispatch_container_register_instance().container_model_name)
        # assert that it is our container
        self.assertTrue(issubclass(obj_cls, TestContainer))
        # get it back, in this case is TestContainer
        user_container = obj_cls.objects.get(**{dispatch_container_register.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_register_instance().container_identifier})
        # assert it is an instance of TestContainer
        self.assertIsInstance(user_container, TestContainer)
        self.assertFalse(user_container.is_dispatched_as_item())
        # dispatch the TestContainer instance
        self.base_dispatch_controller.dispatch_user_container_as_json(user_container)
        # assert that the item was dispacthed to its destination
        self.assertIsInstance(user_container.__class__.objects.using(self.base_dispatch_controller.get_using_destination()).get(pk=user_container.pk), user_container.__class__)
        # assert that the disptched item was tracked in DispatchItemRegister
        self.assertEqual(DispatchItemRegister.objects.all().count(), 1)
        self.assertTrue(DispatchItemRegister.objects.get(item_pk=user_container.pk).is_dispatched)
        # requery for the container instance (Necessary??)
        user_container = obj_cls.objects.get(**{self.base_dispatch_controller.get_dispatch_container_register_instance().container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_register_instance().container_identifier})
        #self.assertTrue(obj.is_dispatched)
        self.assertTrue(user_container.is_dispatched_as_container())
        # assert that you cannot dispatch it again
        self.assertRaises(AlreadyDispatchedItem, self.base_dispatch_controller.dispatch_user_container_as_json, user_container)
        dispatch_item_register = DispatchItemRegister.objects.get(item_pk=user_container.pk)
        # flag is dispatched as False
        dispatch_item_register.is_dispatched = False
        dispatch_item_register.return_datetime = datetime.today()
        dispatch_item_register.save()
        # dispatch again ...
        self.assertIsNone(self.base_dispatch_controller.dispatch_user_container_as_json(user_container))
        # assert that a the existing dispatch item was edited (uses get_or_create)
        self.assertEqual(DispatchItemRegister.objects.all().count(), 1)
        self.assertEqual(DispatchItemRegister.objects.filter(is_dispatched=True, return_datetime__isnull=True).count(), 1)
        #DispatchItemRegister.objects.all().delete()
