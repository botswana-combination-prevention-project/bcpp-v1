from bhp_map.classes import site_mappers
from base_household_mapper import BaseHouseholdMapper
from bcpp_household.choices import OTSE_SECTIONS, OTSE_SUB_SECTIONS, OTSE_LANDMARKS


class OtseHouseholdMapper(BaseHouseholdMapper):

    map_area = 'otse'

    regions = OTSE_SECTIONS
    sections = OTSE_SUB_SECTIONS

    landmarks = OTSE_LANDMARKS

    gps_center_lat = -24.376534
    gps_center_lon = 26.152276
    _radius = 8.699197

site_mappers.register(OtseHouseholdMapper)
