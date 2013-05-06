from django.test import TestCase
from django.db.models import get_app, get_models


class BaseNaturalKeyTests(TestCase):

    def test_for_natural_key(self):
        """Confirms all models have a natural_key method (except Audit models)"""
        for app_label in self.app_labels:
            app = get_app(app_label)
            for model in get_models(app):
                if 'Audit' not in model._meta.object_name:
                    print 'checking for natural key on {0}.'.format(model._meta.object_name)
                    self.assertTrue('natural_key' in dir(model))

    def test_for_get_by_natural_key(self):
        """Confirms all models have a get_by_natural_key manager method."""
        for app_label in self.app_labels:
            app = get_app(app_label)
            for model in get_models(app):
                if 'Audit' not in model._meta.object_name:
                    print 'checking for get_by_natural_key manager method key on {0}.'.format(model._meta.object_name)
                    self.assertTrue('get_by_natural_key' in dir(model.objects))
