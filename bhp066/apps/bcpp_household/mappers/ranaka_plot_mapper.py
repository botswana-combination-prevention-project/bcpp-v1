from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, RANAKA_LANDMARKS


class RanakaPlotMapper(BasePlotMapper):

    map_area = 'ranaka'
    map_code = '11'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = RANAKA_LANDMARKS

    intervention = False

    gps_center_lat = -24.908703
    gps_center_lon = 25.463033
    radius = 4
    location_boundary = ()

site_mappers.register(RanakaPlotMapper)