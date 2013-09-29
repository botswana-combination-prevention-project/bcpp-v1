import sys
import inspect
from django.test import TestCase
from bhp_appointment.tests.factories import ConfigurationFactory


class FactoryTests(TestCase):

    def test(self):
        ConfigurationFactory()

        for name, factory_cls in inspect.getmembers(sys.modules['bcpp_subject.tests.factories']):
            if inspect.isclass(factory_cls):
                if 'subject_visit' in dir(factory_cls.FACTORY_FOR):
                    print factory_cls
                    factory = factory_cls()
                self.assertfactory
