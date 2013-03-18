from bhp_base_model.tests.factories import BaseModelFactory
from django.contrib.contenttypes.models import ContentType


class ContentTypeFactory(BaseModelFactory):
    FACTORY_FOR = ContentType

    name = 'contenttypemap'
    app_label = 'bhp_content_type_map'
    model = 'contenttypemap'
