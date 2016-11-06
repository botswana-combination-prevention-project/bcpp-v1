from django.db import models
from django.conf import settings

from edc_map.site_mappers import site_mappers


class AliquotProcessingManager(models.Manager):

    def get_by_natural_key(self, aliquot_identifier, profile_name):
        return self.get(aliquot__aliquot_identifier=aliquot_identifier, profile__name=profile_name)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            code = site_mappers.get_mapper(site_mappers.current_community).map_code
            return super(AliquotProcessingManager, self).get_queryset().filter(
                aliquot__aliquot_identifier__startswith='066{}'.format(code))
        return super(AliquotProcessingManager, self).get_queryset()
