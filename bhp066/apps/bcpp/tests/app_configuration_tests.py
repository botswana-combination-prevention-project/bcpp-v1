from django.test import TestCase

from edc.core.bhp_variables.models import StudySpecific
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.consent.models import ConsentCatalogue

from ..app_configuration.classes import BcppAppConfiguration

from apps.bcpp_lab.lab_profiles import BcppSubjectProfile


class BcppAppConfigurationTests(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass

    def test_variables_configuration(self):
        self.assertEqual(0, StudySpecific.objects.count())
        BcppAppConfiguration().update_or_create_study_variables()
        self.assertEqual(1, StudySpecific.objects.count())

    def test_consent_catalogue_configuration(self):
        self.assertEqual(0, ConsentCatalogue.objects.count())
        BcppAppConfiguration().update_or_create_consent_catalogue()
        self.assertEqual(1, ConsentCatalogue.objects.count())
