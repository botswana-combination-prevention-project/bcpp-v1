from datetime import datetime
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.conf import settings
from django.test import TestCase
from bhp_registration.models import RegisteredSubject
from bhp_sync.models import Producer, OutgoingTransaction, IncomingTransaction
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.classes import Base, DispatchController
from bhp_dispatch.exceptions import DispatchError, DispatchModelError


class DispatchControllerMethodsTests(TestCase):

    #fixtures = ['test_configuration.json']

    def test_init(self):

        dispatch_url = '/'
        
        # Base tests
        self.assertTrue('DEVICE_ID' in dir(settings), 'Settings attribute DEVICE_ID not found')
        # raise source and destination cannot be the same
        self.assertRaises(DispatchError, Base, 'default', 'default')
        # source must be either server or default
        self.assertRaises(DispatchError, Base, 'not_default', 'default')
        # no producer for destination
        self.assertRaises(DispatchError, Base, 'default', 'dispatch_destination')

        # add a in_active producer
        producer = Producer.objects.create(name='test_producer', settings_key='dispatch_destination', is_active=False)
        self.assertRaises(DispatchError, Base, 'default', 'dispatch_destination')
        # activate producer
        producer.is_active = True
        producer.save()
        self.assertIsInstance(Base('default', 'dispatch_destination'), Base)
        # confirm producer instance is as expected
        self.assertEqual(Base('default', 'dispatch_destination').get_producer(), producer)
        # DATABASE keys check works
        self.assertRaises(ImproperlyConfigured, Base('default', 'dispatch_destination').is_valid_using, 'xdefault', 'source')
        # ...
        self.assertRaises(DispatchError, Base, 'default', 'dispatch_destination', server_device_id=None)
        # id source is default, must be server = 99
        self.assertRaises(DispatchError, Base, 'default', 'dispatch_destination', server_device_id='22')
        #TODO: improve use of DEVICE_ID and server_device_id

        # add outgoing transactions and check is properly detects pending transactions before dispatching
        outgoing_transaction = OutgoingTransaction.objects.using('dispatch_destination').create(
            tx='tx',
            tx_pk='tx_pk',
            producer=producer.name,
            is_consumed=False)
        # create an incoming transaction
        incoming_transaction = IncomingTransaction.objects.using('default').create(
            tx='tx',
            tx_pk='tx_pk',
            producer=producer.name,
            is_consumed=False)
        # create base controller instance
        base_controller = Base('default', 'dispatch_destination')
        # assert there ARE outgoing transactions
        self.assertTrue(base_controller.has_outgoing_transactions())
        # assert there ARE incoming transactions
        self.assertTrue(base_controller.has_incoming_transactions())
        # assert that a dispatch_model_as_json fails due to pending transactions
        self.assertRaises(PendingTransactionError, base_controller.dispatch_model_as_json, None)
        # consume outgoing transaction
        outgoing_transaction.is_consumed = True
        outgoing_transaction.save()
        # assert that a dispatch_model_as_json still fails due to pending transactions
        self.assertRaises(PendingTransactionError, base_controller.dispatch_model_as_json, None)
        # confirm no pending outgoing
        self.assertFalse(base_controller.has_outgoing_transactions())
        # consume incoming transaction
        incoming_transaction.is_consumed = True
        incoming_transaction.save()
        # assert there are no pending incoming transactions
        self.assertFalse(base_controller.has_incoming_transactions())
        # assert there are no pending transactions
        self.assertFalse(base_controller.has_pending_transactions())

        # assert that Base().dispatch_model_as_json must have a model passed to it
        self.assertRaises(DispatchModelError, base_controller.dispatch_model_as_json, None)
        # create a few registsred subject instances
        subject_identifiers = ['subjectA', 'subjectB', 'subjectC']
        for subject_identifier in subject_identifiers:
            RegisteredSubject.objects.create(subject_identifier=subject_identifier)
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
        rs_pks = [rs.pk for rs in RegisteredSubject.objects.all().order_by('id')]
        # assert dispatch_model_as_json accepts RegisteredSubject as a model class
        self.assertEqual(base_controller.dispatch_model_as_json(RegisteredSubject), None)
        # assert number of transactions created on source
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
        # assert RegisteredSubject instances were dispatched
        self.assertEqual([rs.subject_identifier for rs in RegisteredSubject.objects.using('dispatch_destination').all().order_by('subject_identifier')], subject_identifiers)
        self.assertEqual([rs.pk for rs in RegisteredSubject.objects.using('dispatch_destination').all().order_by('id')], rs_pks)
        # confirm no transactions were created anywhere
        self.assertFalse(base_controller.has_pending_transactions())
        # assert that serialize on save signal was disconnected and did not create outgoing transactions
        # while dispatching_model_to_json
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 6)
        # modify a registered subject on the source to create a transaction on the source
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifiers[0])
        registered_subject.registration_status = 'CONSENTED'
        registered_subject.save()
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 8)
        # assert that the transaction is not from the producer
        self.assertFalse(base_controller.has_pending_transactions())
        # modify a registered subject on the destination to create a transaction on the destination
        registered_subject = RegisteredSubject.objects.using('dispatch_destination').get(subject_identifier=subject_identifiers[0])
        registered_subject.registration_status = 'CONSENTED'
        registered_subject.save(using='dispatch_destination')
        #self.assertTrue(base_controller.has_pending_transactions())
        self.assertEquals(OutgoingTransaction.objects.filter(is_consumed=False).count(), 10)
        RegisteredSubject.objects.all().delete()
        RegisteredSubject.objects.using('dispatch_destination').all().delete()
        
        