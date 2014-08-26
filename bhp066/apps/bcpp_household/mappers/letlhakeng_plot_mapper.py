from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LETLHAKENG_LANDMARKS
from ..utils import ClinicDaysTuple


class LetlhakengPlotMapper(BasePlotMapper):

    map_area = 'letlhakeng'
    map_code = '15'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = LETLHAKENG_LANDMARKS

    gps_center_lat = -24.099361
    gps_center_lon = 25.032163
    radius = 5.0
    location_boundary = ()

    intervention = False
    clinic_days = {
        'IDCC': ClinicDaysTuple((MO, WE), None),
        'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 10, 20))}

site_mappers.register(LetlhakengPlotMapper)
