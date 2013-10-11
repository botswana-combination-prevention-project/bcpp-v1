from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MOLAPOWABOJANG_LANDMARKS


class RanakaPlotMapper(BasePlotMapper):

    map_area = 'ranaka'
    map_code = '040'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MOLAPOWABOJANG_LANDMARKS

    gps_center_lat = -24.908703
    gps_center_lon = 25.463033
    radius = 4
    location_boundary = ()
    """([-25.011679818754537, 25.756838464932116], [-25.02619515335593, 25.753326416015625],
                         [-25.03381661473165, 25.755643844604492], [-25.029801706428938, 25.767637448965274],
                         [-25.053490239187333, 25.74920654296875], [-25.059243983236804, 25.73573112487793],
                         [-25.044625834670242, 25.735387802124023], [-25.011679818754537, 25.756838464932116])"""

site_mappers.register(RanakaPlotMapper)