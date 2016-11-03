from django.db import models
from django.db.models import get_model
from django.conf import settings

from edc_map.classes import site_mappers


class HouseholdInfoManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        return self.get(household_structure=household_structure)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(HouseholdInfoManager, self).get_queryset().filter(
                household_structure__household__plot__community=community)
        return super(HouseholdInfoManager, self).get_queryset()
