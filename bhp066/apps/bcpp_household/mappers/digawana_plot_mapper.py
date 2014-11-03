from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, DIGAWANA_LANDMARKS


class DigawanaPlotMapper(BasePlotMapper):

    map_area = 'digawana'
    map_code = '12'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = DIGAWANA_LANDMARKS

    intervention = True

    gps_center_lat = -25.330451
    gps_center_lon = 25.556502
    radius = 3.5
    location_boundary = ()

site_mappers.register(DigawanaPlotMapper)
