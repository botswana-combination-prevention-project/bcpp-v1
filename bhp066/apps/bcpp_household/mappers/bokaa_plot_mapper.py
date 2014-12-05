from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, BOKAA_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


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

    survey_dates = {
        'bcpp-year-1': SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 11, 5),
            full_enrollment_date=date(2014, 11, 28),
            end_date=date(2014, 12, 20),
            smc_start_date=date(2014, 12, 5)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 5),
            full_enrollment_date=date(2015, 11, 28),
            end_date=date(2015, 12, 20),
            smc_start_date=date(2015, 12, 5)),
    }

    clinic_days = {
        'bcpp-year-1': {
            'IDCC': ClinicDaysTuple((WE, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((FR, ), survey_dates['bcpp-year-1'].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((WE, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((FR, ), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(BokaaPlotMapper)
