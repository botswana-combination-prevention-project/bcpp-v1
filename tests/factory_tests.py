from django.test import TestCase
from bhp_content_type_map.classes import ContentTypeMapHelper
from bhp_appointment.tests.factories import ConfigurationFactory
from bhp_content_type_map.models import ContentTypeMap
from factories import TestRequisitionFactory
from bhp_variables.tests.factories import StudySiteFactory, StudySpecificFactory
from bhp_consent.tests.factories import ConsentCatalogueFactory, AttachedModelFactory
from lab_requisition.models import TestRequisition
from bhp_consent.models import TestSubjectConsent, AttachedModel

class FactoryTests(TestCase):

    def setUp(self):
        pass
#         ConfigurationFactory()
#         self.study_site = StudySiteFactory(site_code='10', site_name='TEST_SITE')
#         self.study_specific = StudySpecificFactory()
#         content_type_map_helper = ContentTypeMapHelper()
#         content_type_map_helper.populate()
#         content_type_map_helper.sync()
#         # prepare the consent catalogue
#         content_type_map = ContentTypeMap.objects.get(model__iexact=TestSubjectConsent._meta.object_name)
#         consent_catalogue = ConsentCatalogueFactory(content_type_map=content_type_map)
#         content_type_map = ContentTypeMap.objects.get(model__iexact=TestRequisition._meta.object_name)
#         AttachedModelFactory(consent_catalogue=consent_catalogue, content_type_map=content_type_map)
        

    def test_p1(self):
        "Tests data factories."
        self.assertIsNotNone(TestRequisitionFactory.build())
        self.assertIsNotNone(TestRequisitionFactory.build())
        self.assertIsNotNone(TestRequisitionFactory.build())
        self.assertIsNotNone(TestRequisitionFactory.build())
        self.assertIsNotNone(TestRequisitionFactory.build())
        self.assertIsNotNone(TestRequisitionFactory.build())
        self.assertIsNotNone(TestRequisitionFactory.build())
