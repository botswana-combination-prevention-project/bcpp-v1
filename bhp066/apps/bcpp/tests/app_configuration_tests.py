from django.test import TestCase

from edc.subject.appointment.models import Configuration
from edc.core.bhp_variables.models import StudySpecific
from edc.subject.consent.models import ConsentCatalogue

from ..app_configuration.classes import BcppAppConfiguration


class BcppAppConfigurationTests(TestCase):

    def test_appointment_configuration(self):
        #check that there aren't any configurations in the database
        self.assertEqual(0, Configuration.objects.count())
        #test that the method works
        BcppAppConfiguration().update_or_create_appointment_setup()
        #check that the configuration is created
        self.assertEqual(1, Configuration.objects.count())

    def test_variables_configuration(self):
        self.assertEqual(0, StudySpecific.objects.count())
        BcppAppConfiguration().update_or_create_study_variables()
        self.assertEqual(1, StudySpecific.objects.count())

    def test_consent_catalogue_configuration(self):
        self.assertEqual(0, ConsentCatalogue.objects.count())
        BcppAppConfiguration().update_or_create_consent_catalogue()
        self.assertEqual(1, ConsentCatalogue.objects.count())
