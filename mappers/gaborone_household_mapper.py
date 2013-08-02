from bhp_map.classes import site_mappers
from base_household_mapper import BaseHouseholdMapper
from choices.gaborone import GABORONE_SECTIONS, GABORONE_SUB_SECTIONS, GABORONE_LANDMARKS


class GaboroneHouseholdMapper(BaseHouseholdMapper):

    map_area = 'otse'

    regions = GABORONE_SECTIONS
    sections = GABORONE_SUB_SECTIONS

    landmarks = GABORONE_LANDMARKS

    gps_center_lat = -24.656095
    gps_center_lon = 25.925404
    radius = 5
    location_boundary = ()

site_mappers.register(GaboroneHouseholdMapper)
