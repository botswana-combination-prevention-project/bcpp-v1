from django.conf import settings
from django.db import models

from edc.map.classes import site_mappers


class HouseholdManager(models.Manager):

    def get_by_natural_key(self, household_identifier):
        return self.get(household_identifier=household_identifier)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.current_mapper.map_area
            return super(HouseholdManager, self).get_queryset().filter(plot__community=community)
        return super(HouseholdManager, self).get_queryset()
