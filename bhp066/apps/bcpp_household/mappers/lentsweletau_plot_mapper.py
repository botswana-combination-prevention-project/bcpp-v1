from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LENTSWELETAU_LANDMARKS


class LentsweletauPlotMapper(BasePlotMapper):

    map_area = 'lentsweletau'
    map_code = '16'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = LENTSWELETAU_LANDMARKS

    gps_center_lat = -24.252443
    gps_center_lon = 25.854249
    radius = 5.0
    location_boundary = ()

site_mappers.register(LentsweletauPlotMapper)
