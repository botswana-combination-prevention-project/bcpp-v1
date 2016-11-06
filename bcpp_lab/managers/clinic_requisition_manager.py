from django.db import models
from django.conf import settings

from edc_map.site_mappers import site_mappers


class ClinicRequisitionManager(models.Manager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(ClinicRequisitionManager, self).get_queryset().filter(community=community)
        return super(ClinicRequisitionManager, self).get_queryset()
