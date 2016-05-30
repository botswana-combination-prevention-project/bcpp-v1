from django.conf import settings

from edc_map.classes import site_mappers

from lis.specimen.lab_aliquot.managers import AliquotManager as BaseAliquotManager


class AliquotManager(BaseAliquotManager):

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            code = site_mappers.get_mapper(site_mappers.current_community).map_code
            return super(AliquotManager, self).get_queryset().filter(
                aliquot_identifier__startswith='066{}'.format(code))
        return super(AliquotManager, self).get_queryset()
