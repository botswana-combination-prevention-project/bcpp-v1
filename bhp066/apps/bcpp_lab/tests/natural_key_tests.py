from datetime import datetime
from django.test import TestCase
from django.core import serializers
from django.db.models import get_app, get_models

from edc.core.crypto_fields.classes import FieldCryptor
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.device.sync.classes import SerializeToTransaction
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from apps.bcpp.app_configuration.classes import BcppAppConfiguration
from apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from apps.bcpp_lab.models import (Panel,AliquotType,Profile,ProfileItem,AliquotCondition)
#from .factories import ()


class NaturalKeyTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name and model._meta.object_name not in ['PackingList', 'Receive', 'PackingListItem', 'Processing']:
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_lab')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name and model._meta.object_name not in ['PackingList', 'Receive', 'PackingListItem', 'Processing']:
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))

    def test_p3(self):
        instances = []
        instances.append(Panel.objects.all()[0])
        instances.append(Panel.objects.all()[1])
        instances.append(AliquotType.objects.all()[0])
        instances.append(AliquotType.objects.all()[1])
        instances.append(Profile.objects.all()[0])
        instances.append(Profile.objects.all()[1])
        instances.append(ProfileItem.objects.all()[1])
        instances.append(ProfileItem.objects.all()[1])
        #aliquot_condition = AliquotCondition
        print 'INSTANCE: ' + str(instances)
        for obj in instances:
            print 'test natural key on {0}'.format(obj._meta.object_name)
            natural_key = obj.natural_key()
            get_obj = obj.__class__.objects.get_by_natural_key(*natural_key)
            self.assertEqual(obj.pk, get_obj.pk)
        # pp = pprint.PrettyPrinter(indent=4)
        for obj in instances:
            print 'test serializing/deserializing {0}'.format(obj._meta.object_name)
            outgoing_transaction = SerializeToTransaction().serialize(obj.__class__, obj)
            # pp.pprint(FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx))
            for transaction in serializers.deserialize("json", FieldCryptor('aes', 'local').decrypt(outgoing_transaction.tx)):
                self.assertEqual(transaction.object.pk, obj.pk)