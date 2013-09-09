from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_sync.models import Producer


class ProducerFactory(BaseUuidModelFactory):
    FACTORY_FOR = Producer

    name = 'producer'
    settings_key = 'dispatch_destination'
    url = 'http://'
