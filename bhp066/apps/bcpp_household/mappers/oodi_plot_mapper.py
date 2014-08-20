from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, OODI_LANDMARKS


class OodiPlotMapper(BasePlotMapper):

    map_area = 'oodi'
    map_code = '18'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = OODI_LANDMARKS

    enhanced_care = True

    gps_center_lat = -24.425856
    gps_center_lon = 26.021626
    radius = 5.5
    location_boundary = ()

site_mappers.register(OodiPlotMapper)
