from django.db.models import get_app, get_models

from django.test import TestCase


class NaturalKeyTests(TestCase):

    def test_p1(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        app = get_app('bcpp_rbd')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name and model._meta.object_name != 'RBDEligibility':
                print 'checking for natural key on {0}.'.format(model._meta.object_name)
                self.assertTrue('natural_key' in dir(model), 'natural key not found in {0}'.format(model._meta.object_name))

    def test_p2(self):
        """Confirms all models have a get_by_natural_key manager method."""
        app = get_app('bcpp_rbd')
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name and model._meta.object_name != 'RBDEligibility':
                print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                self.assertTrue('get_by_natural_key' in dir(model.objects), 'get_by_natural_key key not found in {0}'.format(model._meta.object_name))
