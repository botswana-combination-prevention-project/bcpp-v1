from django.db import models
from django.conf import settings

from edc.map.classes import site_mappers


class SubjectRequisitionManager(models.Manager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            return super(SubjectRequisitionManager, self).get_queryset().filter(community=community)
        return super(SubjectRequisitionManager, self).get_queryset()
