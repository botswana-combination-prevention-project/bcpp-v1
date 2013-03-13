import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from bhp_content_type_map.models import ContentTypeMap
from bhp_sync.classes import Consumer, DeserializeFromTransaction, SerializeToTransaction
from bhp_consent.models import ConsentCatalogue
from bhp_sync.models import Producer, OutgoingTransaction, IncomingTransaction, TestItem


class TransactionTests(TestCase):

    def setUp(self):
        self.producer = None
        self.using_destination = 'dispatch_destination'
        self.using_source = 'default'
        Producer.objects.using(self.using_source).delete()
        OutgoingTransaction.objects.using(self.using_destination).delete()
        IncomingTransaction.objects.using(self.using_source).delete()

    def create_producer(self, is_active=False):
        # add a in_active producer
        self.producer = Producer.objects.create(name='test_producer', settings_key=self.using_destination, is_active=is_active)

    def create_test_item(self, identifier, using=None):
        return TestItem.objects.using(using).create(test_item_identifier=identifier, comment='TEST_COMMENT')

    def test_transactions_p1(self):
        TestItem.objects.all().delete()
        TestItem.objects.using(self.using_destination).all().delete()
        OutgoingTransaction.objects.all().delete()
        OutgoingTransaction.objects.using(self.using_destination).all().delete()
        IncomingTransaction.objects.all().delete()
        IncomingTransaction.objects.using(self.using_source).all().delete()
        Producer.objects.using(self.using_source).delete()
        self.create_producer()
        # create a test item on source
        src_item = self.create_test_item('SRC_IDENTIFIER', self.using_source)
        # assert outgoing transactions on source
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name=src_item._meta.object_name, tx_pk=src_item.pk).count(), 1)
        # assert NO outgoing transactions on destination
        self.assertEqual(OutgoingTransaction.objects.using(self.using_destination).filter(tx_name=src_item._meta.object_name, tx_pk=src_item.pk).count(), 0)
        # create a test item on using_destination
        dst_item = self.create_test_item('DST_IDENTIFIER', self.using_destination)
        # assert NO outgoing transactions on source
        self.assertEqual(OutgoingTransaction.objects.filter(tx_name=dst_item._meta.object_name, tx_pk=dst_item.pk).count(), 0)
        # assert outgoing transactions on destination
        self.assertEqual(OutgoingTransaction.objects.using(self.using_destination).filter(tx_name=dst_item._meta.object_name, tx_pk=dst_item.pk).count(), 1)

    def test_transactions_p2(self):
        TestItem.objects.all().delete()
        TestItem.objects.using(self.using_destination).all().delete()
        OutgoingTransaction.objects.all().delete()
        OutgoingTransaction.objects.using(self.using_destination).all().delete()
        IncomingTransaction.objects.all().delete()
        IncomingTransaction.objects.using(self.using_source).all().delete()
        Producer.objects.using(self.using_source).delete()
        self.create_producer()
        # create a test item on source
        src_item = self.create_test_item('SRC_IDENTIFIER', self.using_source)
        self.assertEqual(src_item.comment, 'TEST_COMMENT')
        # serialize to destination
        serialize_to_transaction = SerializeToTransaction()
        serialize_to_transaction.serialize(src_item.__class__, src_item, using=self.using_destination)
        # change on destination
        dst_item = TestItem.objects.using(self.using_source).get(test_item_identifier='SRC_IDENTIFIER')
        self.assertEqual(dst_item.comment, 'TEST_COMMENT')
        dst_item.comment = 'HELLO FROM DST'
        dst_item.save()
        # sync back to source
        consumer = Consumer()
        consumer.fetch_from_producer(self.using_destination)
        # verify updated
        src_item = TestItem.objects.get(test_item_identifier='SRC_IDENTIFIER')
        self.assertEqual(src_item.comment, 'HELLO FROM DST')


        