import re
from django.test import TestCase
from django.conf import settings
from bhp_consent.models import ConsentCatalogue
from bhp_consent.tests.factories import ConsentCatalogueFactory


class ModelTests(TestCase):

    def test_p1(self):
        for cls, cls_factory in [(ConsentCatalogue, ConsentCatalogueFactory)]:
            print 'using {0}'.format(cls._meta.object_name)
            print 'test {0} natural key'.format(cls._meta.object_name)
            rs1 = cls_factory()
            args = rs1.natural_key()
            rs2 = cls.objects.get_by_natural_key(*args)
            self.assertEqual(rs1, rs2)
