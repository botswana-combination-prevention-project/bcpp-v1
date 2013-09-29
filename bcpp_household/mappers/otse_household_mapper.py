from edc_core.bhp_map.classes import site_mappers
from .base_household_mapper import BaseHouseholdMapper
from .choices import OTSE_SECTIONS, OTSE_SUB_SECTIONS, OTSE_LANDMARKS


class OtseHouseholdMapper(BaseHouseholdMapper):

    map_area = 'otse'
    map_code = '198'
    regions = OTSE_SECTIONS
    sections = OTSE_SUB_SECTIONS

    landmarks = OTSE_LANDMARKS

    gps_center_lat = -25.033194
    gps_center_lon = 25.747132
    radius = 5.5
    location_boundary = ()
    """([-25.011679818754537, 25.756838464932116], [-25.02619515335593, 25.753326416015625],
                         [-25.03381661473165, 25.755643844604492], [-25.029801706428938, 25.767637448965274],
                         [-25.053490239187333, 25.74920654296875], [-25.059243983236804, 25.73573112487793],
                         [-25.044625834670242, 25.735387802124023], [-25.011679818754537, 25.756838464932116])"""

site_mappers.register(OtseHouseholdMapper)
