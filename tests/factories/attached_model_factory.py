import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_consent.tests.factories import ConsentCatalogueFactory
from bhp_content_type_map.tests.factories import ContentTypeMapFactory
from bhp_consent.models import AttachedModel


class AttachedModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = AttachedModel

    consent_catalogue = factory.SubFactory(ConsentCatalogueFactory)
    content_type_map = '' # factory.SubFactory(ContentTypeMapFactory, content_type=factory.SelfAttribute('..content_type_map.content_type'))
    is_active = True
