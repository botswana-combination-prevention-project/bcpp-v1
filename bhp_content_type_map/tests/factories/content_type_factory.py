import factory
from bhp_base_model.tests.factories import BaseModelFactory
from django.contrib.contenttypes.models import ContentType


class ContentTypeFactory(BaseModelFactory):
    FACTORY_FOR = ContentType

    name = factory.Sequence(lambda n: 'contenttypemap{0}'.format(n))
    app_label = 'bhp_content_type_map'
    model = factory.Sequence(lambda n: 'contenttypemap{0}'.format(n))
