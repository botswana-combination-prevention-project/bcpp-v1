from dateutil.relativedelta import MO, TU, WE, TH, FR

from datetime import date
from edc.map.classes import site_mappers
from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, OODI_LANDMARKS

from ..utils import ClinicDaysTuple


class OodiPlotMapper(BasePlotMapper):

    map_area = 'oodi'
    map_code = '18'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = OODI_LANDMARKS

    intervention = True

    gps_center_lat = -24.425856
    gps_center_lon = 26.021626
    radius = 300
    location_boundary = ()

    bhs_start_date = date(2014, 11, 5)
    bhs_full_enrollment_date = date(2014, 11, 28)
    bhs_end_date = date(2014, 12, 20)
    smc_start_date = date(2014, 12, 8)  # referenced by bcpp mappers

    clinic_days = {
        'IDCC': ClinicDaysTuple((MO, ), None),
        'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), smc_start_date)}

site_mappers.register(OodiPlotMapper)
