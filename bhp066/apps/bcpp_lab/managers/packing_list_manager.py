from django.db.models import Manager
from django.conf import settings

from edc.map.classes import site_mappers


class PackingListManager(Manager):

    def get_by_natural_key(self, timestamp):
        return self.get(timestamp=timestamp)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(PackingListManager, self).get_queryset().filter(community=community)
        return super(PackingListManager, self).get_queryset()


class PackingListItemManager(Manager):

    def get_by_natural_key(self, item_reference):
        return self.get(item_reference=item_reference)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(PackingListItemManager, self).get_queryset().filter(packing_list__community=community)
        return super(PackingListItemManager, self).get_queryset()
