import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_visit.models import VisitDefinition
from bhp_content_type_map.tests.factories import ContentTypeMapFactory

starting_seq_num = 1000


class VisitDefinitionFactory(BaseUuidModelFactory):
    FACTORY_FOR = VisitDefinition
    code = factory.Sequence(lambda n: 'CODE{0}'.format(n))
    title = factory.LazyAttribute(lambda o: 'TITLE{0}'.format(o.code))
    visit_tracking_content_type_map = factory.SubFactory(ContentTypeMapFactory)
