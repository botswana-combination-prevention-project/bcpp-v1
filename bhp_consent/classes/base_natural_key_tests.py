import pprint
from django.core import serializers
from django.test import TestCase
from django.db.models import get_app, get_models
from bhp_sync.classes import SerializeToTransaction, DeserializeFromTransaction
from bhp_crypto.classes import FieldCryptor



class BaseNaturalKeyTests(TestCase):

    def test_for_natural_key(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app(self.app_label)
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural_key method not found on model {0}'.format(model._meta.object_name))

    def test_for_get_by_natural_key(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app(self.app_label)
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key manager method not found on model {0}.'.format(model._meta.object_name))

    def serialize_deserialize(self, instances):
        """Serializes then deserializes a list of instances."""
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)

        pp = pprint.PrettyPrinter(indent=4)

        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)
