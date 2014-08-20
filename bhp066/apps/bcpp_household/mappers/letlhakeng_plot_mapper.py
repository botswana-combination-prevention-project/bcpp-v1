from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LETLHAKENG_LANDMARKS


class LetlhakengPlotMapper(BasePlotMapper):

    map_area = 'letlhakeng'
    map_code = '15'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = LETLHAKENG_LANDMARKS

    enhanced_care = False

    gps_center_lat = -24.099361
    gps_center_lon = 25.032163
    radius = 5.0
    location_boundary = ()

site_mappers.register(LetlhakengPlotMapper)
