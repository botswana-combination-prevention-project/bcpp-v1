from bhp_map.classes import site_mapper
from base_household_mapper import BaseHouseholdMapper
from bcpp_household.choices import OTSE_WARDS, OTSE_WARD_SECTIONS, OTSE_LANDMARKS


class OtseHouseholdMapper(BaseHouseholdMapper):

    map_area = 'otse'

    regions = OTSE_WARDS
    sections = OTSE_WARD_SECTIONS

    landmarks = OTSE_LANDMARKS

    gps_center_lat = -24.376534
    gps_center_lon = 26.152276
    gps_radius = 8.699197

site_mapper.register(OtseHouseholdMapper)
