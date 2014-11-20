from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MOLAPOWABOJANG_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


class MolapowabojangPlotMapper(BasePlotMapper):

    map_area = 'molapowabojang'
    map_code = '13'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MOLAPOWABOJANG_LANDMARKS

    intervention = False

    gps_center_lat = -25.204009
    gps_center_lon = 25.562754
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        'bcpp-year-1': SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 11, 5),
            full_enrollment_date=date(2014, 11, 28),
            end_date=date(2014, 12, 20),
            smc_start_date=date(2014, 12, 1)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 5),
            full_enrollment_date=date(2015, 11, 28),
            end_date=date(2015, 12, 20),
            smc_start_date=date(2015, 12, 1)),
    }

    clinic_days = {
        'bcpp-year-1': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-1'].smc_start_date)},
    }

site_mappers.register(MolapowabojangPlotMapper)
