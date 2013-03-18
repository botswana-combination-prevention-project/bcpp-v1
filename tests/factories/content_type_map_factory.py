import factory
from bhp_base_model.tests.factories import BaseModelFactory
from bhp_content_type_map.models import ContentTypeMap
from content_type_factory import ContentTypeFactory


class ContentTypeMapFactory(BaseModelFactory):
    FACTORY_FOR = ContentTypeMap

    content_type = factory.SubFactory(ContentTypeFactory)
    name = factory.LazyAttribute(lambda o: '{0}'.format(o.content_type.model_class()._meta.verbose_name))
    app_label = factory.LazyAttribute(lambda o: '{0}'.format(o.content_type.model_class()._meta.app_label))
    model = factory.LazyAttribute(lambda o: '{0}'.format(o.content_type.model_class()._meta.object_name))
