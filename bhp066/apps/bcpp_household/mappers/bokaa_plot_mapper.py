from dateutil.relativedelta import MO, TU, WE, TH, FR

from datetime import date
from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, BOKAA_LANDMARKS

from ..utils import ClinicDaysTuple


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

    bhs_start_date = date(2014, 11, 5)
    bhs_full_enrollment_date = date(2014, 11, 28)
    bhs_end_date = date(2014, 12, 20)
    smc_start_date = date(2014, 12, 5)  # referenced by bcpp mappers

    clinic_days = {
        'IDCC': ClinicDaysTuple((WE, ), None),
        'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'SMC': ClinicDaysTuple((FR, ), smc_start_date)}

site_mappers.register(BokaaPlotMapper)
