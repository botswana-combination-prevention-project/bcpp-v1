from django.db import models
from bhp_entry.managers import BaseEntryBucketManager
from bhp_content_type_map.models import ContentTypeMap
from bhp_visit.models import VisitDefinition


class EntryBucketManager(models.Manager):
    def get_by_natural_key(self, visit_definition, app_label, model):
        visit_definition = VisitDefinition.objects.get(code=visit_definition)
        content_map_type = ContentTypeMap.objects.get(
            app_label=app_label,
            model=model
            )
        return self.get(
            content_map_type=content_map_type,
            visit_definition=visit_definition
            )
