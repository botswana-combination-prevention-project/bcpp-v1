from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, GABORONE_LANDMARKS


class GaboronePlotMapper(BasePlotMapper):

    map_area = 'gaborone'
    map_code = '070'

    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = GABORONE_LANDMARKS

    gps_center_lat = -24.656095
    gps_center_lon = 25.925404
    radius = 15
    location_boundary = ()

site_mappers.register(GaboronePlotMapper)