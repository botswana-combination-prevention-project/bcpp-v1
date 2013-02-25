from django.test import TestCase
from bhp_sync.models import Producer, OutgoingTransaction, IncomingTransaction
from bhp_dispatch.models import TestItem, DispatchItem, DispatchContainer
from bhp_dispatch.classes import BaseDispatchController


class BaseControllerTests(TestCase):

    def setUp(self):
        self.base_dispatch_controller = None
        self.producer = None
        self.outgoing_transaction = None
        self.incoming_transaction = None
        self.using_source = 'default'
        self.using_destination = 'dispatch_destination'
        self.dispatch_container_app_label = 'bhp_dispatch'
        self.dispatch_container_model_name = 'testitem'
        self.dispatch_container_identifier_attrname = 'test_item_identifier'
        self.dispatch_container_identifier = 'TEST_IDENTIFIER'
        self.dispatch_item_app_label = 'bhp_dispatch'  # usually something like 'mochudi_subject'
        DispatchContainer.objects.all().delete()
        DispatchItem.objects.all().delete()

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

    def create_base_dispatch_controller(self):
        # create base controller instance
        self.base_dispatch_controller = BaseDispatchController(self.using_source, self.using_destination,
                                                self.dispatch_container_app_label,
                                                self.dispatch_container_model_name,
                                                self.dispatch_container_identifier_attrname,
                                                self.dispatch_container_identifier,
                                                self.dispatch_item_app_label)
