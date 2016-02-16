from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers


class ReplacementHistoryManager(models.Manager):

    def get_by_natural_key(self, replacing_item, replaced_item):
        return self.get(replacing_item=replacing_item, replaced_item=replaced_item)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(ReplacementHistoryManager, self).get_queryset().filter(
                replacing_item__startswith=community)
        return super(ReplacementHistoryManager, self).get_queryset()
