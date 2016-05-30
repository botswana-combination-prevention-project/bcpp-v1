from django.db.models import Manager
from django.conf import settings

from edc_map.classes import site_mappers


class ReceiveManager(Manager):

    def get_by_natural_key(self, receive_identifier):
        return self.get(receive_identifier=receive_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            code = site_mappers.get_mapper(site_mappers.current_community).map_code
            return super(ReceiveManager, self).get_queryset().filter(
                receive_identifier__startswith='066{}'.format(code))
        return super(ReceiveManager, self).get_queryset()
