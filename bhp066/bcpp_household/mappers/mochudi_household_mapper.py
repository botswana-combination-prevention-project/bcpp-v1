from edc_core.bhp_map.classes import site_mappers
from .base_household_mapper import BaseHouseholdMapper
from .choices import MOCHUDI_SECTIONS, MOCHUDI_SUB_SECTIONS, MOCHUDI_LANDMARKS


class MochudiHouseholdMapper(BaseHouseholdMapper):
    map_area = 'mochudi'
    map_code = '020'
    regions = MOCHUDI_SECTIONS
    sections = MOCHUDI_SUB_SECTIONS
    landmarks = MOCHUDI_LANDMARKS
    gps_center_lat = -24.390254
    gps_center_lon = 26.158733
    radius = 9.5
    location_boundary = ()

site_mappers.register(MochudiHouseholdMapper)
