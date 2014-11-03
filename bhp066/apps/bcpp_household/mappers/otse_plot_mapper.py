from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, OTSE_LANDMARKS


class OtsePlotMapper(BasePlotMapper):

    map_area = 'otse'
    map_code = '14'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = OTSE_LANDMARKS

    intervention = True

    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()

site_mappers.register(OtsePlotMapper)
