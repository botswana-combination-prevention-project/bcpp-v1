from django.apps import apps as django_apps
from django.conf import settings
from django.db import models

from edc_map.site_mappers import site_mappers


class HouseholdInfoManager(models.Manager):

    def get_by_natural_key(self, household_identifier, survey_name):
        HouseholdStructure = django_apps.get_model('bcpp_household', 'HouseholdStructure')
        household_structure = HouseholdStructure.objects.get_by_natural_key(household_identifier, survey_name)
        return self.get(household_structure=household_structure)

    def get_queryset(self):
        if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
            community = site_mappers.get_mapper(site_mappers.current_community).map_area
            return super(HouseholdInfoManager, self).get_queryset().filter(
                household_structure__household__plot__community=community)
        return super(HouseholdInfoManager, self).get_queryset()
