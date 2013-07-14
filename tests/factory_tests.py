import sys
import inspect
from django.test import TestCase
#from bcpp_subject.tests import factories


class FactoryTests(TestCase):

    def test(self):
        for name, factory_cls in inspect.getmembers(sys.modules['bcpp_subject.tests.factories']):
            if inspect.isclass(factory_cls):
                if 'subject_visit' in dir(factory_cls.FAVTORY_FOR):
                    print factory_cls
                    factory = factory_cls()
                self.assertfactory
