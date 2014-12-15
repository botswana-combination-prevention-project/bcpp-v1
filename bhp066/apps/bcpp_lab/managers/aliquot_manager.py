from django.conf import settings

from edc.map.classes import site_mappers

from lis.specimen.lab_aliquot.managers import AliquotManager


class AliquotManager(AliquotManager):

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            code = site_mappers.current_mapper.map_code
            return super(AliquotManager, self).get_queryset().filter(
                aliquot_identifier__startswith='066{}'.format(code))
        return super(AliquotManager, self).get_queryset()
