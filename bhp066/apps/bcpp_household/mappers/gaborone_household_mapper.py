from edc.map.classes import site_mappers
from .choices.gaborone import GABORONE_SECTIONS, GABORONE_SUB_SECTIONS, GABORONE_LANDMARKS
from .base_household_mapper import BaseHouseholdMapper


class GaboroneHouseholdMapper(BaseHouseholdMapper):

    map_area = 'gaborone'
    map_code = '040'

    regions = GABORONE_SECTIONS
    sections = GABORONE_SUB_SECTIONS

    landmarks = GABORONE_LANDMARKS

    gps_center_lat = -24.656095
    gps_center_lon = 25.925404
    radius = 5
    location_boundary = ()

site_mappers.register(GaboroneHouseholdMapper)
