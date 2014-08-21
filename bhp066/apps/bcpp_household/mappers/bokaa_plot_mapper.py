from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, BOKAA_LANDMARKS


class BokaaPlotMapper(BasePlotMapper):

    map_area = 'bokaa'
    map_code = '17'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = BOKAA_LANDMARKS

    intervention = False

    gps_center_lat = -24.425856
    gps_center_lon = 26.021626
    radius = 5.5
    location_boundary = ()

site_mappers.register(BokaaPlotMapper)
