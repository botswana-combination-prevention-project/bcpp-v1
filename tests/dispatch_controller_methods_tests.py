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
from base_controller_tests import BaseControllerTests


class DispatchControllerMethodsTests(BaseControllerTests):

    #fixtures = ['test_configuration.json']

#    def setUp(self):
#        super(DispatchControllerMethodsTests, self).setUp()

    def create_test_item(self):
        self.test_item = TestItem.objects.create(test_item_identifier=self.dispatch_container_identifier)

    def create_producer(self, is_active=False):
        # add a in_active producer
        self.producer = Producer.objects.create(name='test_producer', settings_key=self.using_destination, is_active=is_active)

    def create_sync_transactions(self):
                # add outgoing transactions and check is properly detects pending transactions before dispatching
        self.outgoing_transaction = OutgoingTransaction.objects.using(self.using_destination).create(
            tx='tx',
            tx_pk='tx_pk',
            producer=self.producer.name,
            is_consumed=False)
        # create an incoming transaction
        self.incoming_transaction = IncomingTransaction.objects.using(self.using_source).create(
            tx='tx',
            tx_pk='tx_pk',
            producer=self.producer.name,
            is_consumed=False)

    def test_base_methods(self):
        # Base tests
        self.assertTrue('DEVICE_ID' in dir(settings), 'Settings attribute DEVICE_ID not found')
        # raise source and destination cannot be the same
        self.assertRaises(DispatchError, Base, self.using_source, self.using_source)
        # source must be either server or default
        self.assertRaises(DispatchError, Base, 'not_default', self.using_source)
        # no producer for destination
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination)
        self.create_producer()
        self.assertIsInstance(self.producer, Producer)
        # no active producer for destination
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination)
        # activate producer
        self.producer.is_active = True
        self.producer.save()
        # Base instance creates OK
        self.assertIsInstance(Base(self.using_source, self.using_destination), Base)
        # confirm producer instance is as expected
        self.assertEqual(Base(self.using_source, self.using_destination).get_producer(), self.producer)
        # DATABASE keys check works
        self.assertRaises(ImproperlyConfigured, Base(self.using_source, self.using_destination).is_valid_using, 'xdefault', 'source')
        # ...
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination, server_device_id=None)
        # id source is default, must be server = 99
        self.assertRaises(DispatchError, Base, self.using_source, self.using_destination, server_device_id='22')
        #TODO: improve use of DEVICE_ID and server_device_id
        Producer.objects.all().delete()

    def test_base_dispatch_methods(self):
        self.create_producer(True)
        # add outgoing transactions and check is properly detects pending transactions before dispatching
        self.create_sync_transactions()
        # create an instance for the user container model
        # ... try get_model with self attributes first
        self.assertIsNotNone(get_model(self.dispatch_container_app_label, self.dispatch_container_model_name))
        self.create_test_item()
        # assert test_item instance created
        self.assertIsInstance(self.test_item, TestItem)
        self.assertEqual(TestItem.objects.filter(**{self.dispatch_container_identifier_attrname: self.dispatch_container_identifier}).count(), 1)
        self.assertEqual(getattr(TestItem.objects.get(**{self.dispatch_container_identifier_attrname: self.dispatch_container_identifier}), self.dispatch_container_identifier_attrname), self.dispatch_container_identifier)
        # assert Trasactions created
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 2)
        # consume the OutgoingTransactions created by creating TestItem
        OutgoingTransaction.objects.all().update(is_consumed=True)

        # create base controller instance
        self.create_base_dispatch_controller()

        # assert there ARE outgoing transactions
        self.assertTrue(self.base_dispatch_controller.has_outgoing_transactions())
        # assert there ARE incoming transactions
        self.assertTrue(self.base_dispatch_controller.has_incoming_transactions(RegisteredSubject))
        # assert that Base().dispatch_model_as_json must have a model passed to it
        # self.assertRaises(DispatchModelError, base_dispatch_controller.dispatch_as_json, None)
        # assert that a dispatch_model_as_json fails due to pending transactions
        self.assertRaises(PendingTransactionError, self.base_dispatch_controller.dispatch_as_json, RegisteredSubject)
        # consume outgoing transaction
        self.outgoing_transaction.is_consumed = True
        self.outgoing_transaction.save()
        # assert that a dispatch_model_as_json still fails due to pending transactions
        self.assertRaises(PendingTransactionError, self.base_dispatch_controller.dispatch_as_json, RegisteredSubject)
        # confirm no pending outgoing
        self.assertFalse(self.base_dispatch_controller.has_outgoing_transactions())
        # consume incoming transaction
        self.incoming_transaction.is_consumed = True
        self.incoming_transaction.save()
        # assert there are no pending incoming transactions
        self.assertFalse(self.base_dispatch_controller.has_incoming_transactions(RegisteredSubject))
        # assert there are no pending transactions
        self.assertFalse(self.base_dispatch_controller.has_pending_transactions(RegisteredSubject))

        # create a few registsred subject instances
        subject_identifiers = ['subjectA', 'subjectB', 'subjectC']
        for subject_identifier in subject_identifiers:
            RegisteredSubject.objects.create(subject_identifier=subject_identifier)
        # assert that outgoing transactions were created (2 for each -- one for model, one for audit)
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
        rs_pks = [rs.pk for rs in RegisteredSubject.objects.all().order_by('id')]
        # assert dispatch_model_as_json accepts RegisteredSubject as a model class
        self.assertEqual(self.base_dispatch_controller.dispatch_model_as_json(RegisteredSubject), None)
        # assert dispatch_as_json does not create any sync transactions
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
        # assert that RegisteredSubject instance is already dispatched
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifiers[0])
        self.assertRaises(AlreadyDispatched, registered_subject.save)
        # flag as dispatched
        DispatchItem.objects.all().update(is_dispatched=False)
        # assert deleting dispatch items does not create transactions
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
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
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 10)
        RegisteredSubject.objects.all().delete()
        RegisteredSubject.objects.using(self.using_destination).all().delete()
        DispatchContainer.objects.all().delete()

    def test_get_scheduled_models(self):
        self.create_producer(True)
        self.create_test_item()
        # create base controller instance
        self.create_base_dispatch_controller()
        # assert that the dispatch item app is set (set in setUp)
        self.assertIsNotNone(self.base_dispatch_controller.get_dispatch_item_app_label())
        # get the scheduled models
        scheduled_models = self.base_dispatch_controller.get_scheduled_models()
        # assert that return value is a list
        self.assertIsInstance(scheduled_models, list)
        # assert that some scheduled model classes were returned
        self.assertGreaterEqual(len(scheduled_models), 0)
        # assert that returned list contains classes that are subclassed from BaseConsentedUuidModel
        # ... must be true for all scheduled models in an app.
        for scheduled_model in scheduled_models:
            self.assertTrue(issubclass(scheduled_model, BaseConsentedUuidModel))

    def test_get_membershipform_models(self):
        self.create_producer(True)
        self.create_test_item()
        # create base controller instance
        self.create_base_dispatch_controller()
        membershipform_models = self.base_dispatch_controller.get_membershipform_models()
        self.assertIsInstance(membershipform_models, list)
        for membershipform_model in membershipform_models:
            self.assertTrue(hasattr(membershipform_model, 'registered_subject'))

    def test_dispatch(self):
        self.create_producer(True)
        self.create_test_item()
        # create base controller instance
        self.create_base_dispatch_controller()
        dispatch_container = self.base_dispatch_controller.get_dispatch_container_instance()
        obj_cls = get_model(
            self.base_dispatch_controller.get_dispatch_container_instance().container_app_label,
            self.base_dispatch_controller.get_dispatch_container_instance().container_model_name)
        obj = obj_cls.objects.get(**{dispatch_container.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_instance().container_identifier})
        self.base_dispatch_controller.dispatch_as_json(obj)
        # assert that the item was dispacthed to its destination
        self.assertIsInstance(obj.__class__.objects.using(self.base_dispatch_controller.get_using_destination()).get(pk=obj.pk), obj.__class__)
        # assert that the disptched item was tracked in DispatchItem
        self.assertEqual(DispatchItem.objects.all().count(), 1)
        self.assertTrue(DispatchItem.objects.get(item_pk=obj.pk).is_dispatched)
        # requery for the container instance (Necessary??)
        obj = obj_cls.objects.get(**{dispatch_container.container_identifier_attrname: self.base_dispatch_controller.get_dispatch_container_instance().container_identifier})
        #self.assertTrue(obj.is_dispatched)
        self.assertTrue(obj.is_dispatched_to_producer())
        # assert that you cannot dispatch it again
        self.assertRaises(AlreadyDispatched, self.base_dispatch_controller.dispatch_as_json, obj)
        dispatch_item = DispatchItem.objects.get(item_pk=obj.pk)
        # flag is dispatched as False
        dispatch_item.is_dispatched = False
        dispatch_item.return_datetime = datetime.today()
        dispatch_item.save()
        # dispatch again ...
        self.assertIsNone(self.base_dispatch_controller.dispatch_as_json(obj))
        # assert that a new dispatch item was created
        self.assertEqual(DispatchItem.objects.all().count(), 2)
        DispatchItem.objects.all().delete()
