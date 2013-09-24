import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_content_type_map.tests.factories import ContentTypeMapFactory
from bhp_consent.models import ConsentCatalogue


class ConsentCatalogueFactory(BaseUuidModelFactory):
    FACTORY_FOR = ConsentCatalogue

    name = 'consent'
    content_type_map = factory.SubFactory(ContentTypeMapFactory)
    consent_type = 'study'
    version = '1'
    start_datetime = datetime(datetime.today().year - 1, 1, 1)
    end_datetime = datetime(datetime.today().year + 5, 1, 1)
    add_for_app = None
