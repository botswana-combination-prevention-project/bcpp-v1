from django.db import models
from bhp_content_type_map.models import ContentTypeMap
from bhp_visit.models import VisitDefinition


class EntryBucketManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, app_label, model):
        """Returns the instance using the natural key."""
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        content_map_type = ContentTypeMap.objects.get_by_natural_key(app_label, model)
        return self.get(content_map_type=content_map_type, visit_definition=visit_definition)
