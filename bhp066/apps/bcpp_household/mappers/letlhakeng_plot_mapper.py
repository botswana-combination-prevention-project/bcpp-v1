from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LETLHAKENG_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


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

    survey_dates = {
        'bcpp-year-1': SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 9, 5),
            full_enrollment_date=date(2014, 10, 15),
            end_date=date(2014, 10, 21),
            smc_start_date=date(2014, 10, 29)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 9, 5),
            full_enrollment_date=date(2015, 10, 15),
            end_date=date(2015, 10, 21),
            smc_start_date=date(2015, 10, 29)),
    }

    clinic_days = {
        'bcpp-year-1': {
            'IDCC': ClinicDaysTuple((TU, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((WE, ), survey_dates['bcpp-year-1'].smc_start_date)},
    }

site_mappers.register(LetlhakengPlotMapper)
