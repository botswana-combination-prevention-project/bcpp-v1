from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, DIGAWANA_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


class TestPlotMapper(BasePlotMapper):

    map_area = 'test_community'
    map_code = '01'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = DIGAWANA_LANDMARKS

    gps_center_lat = -25.330451
    gps_center_lon = 25.556502
    radius = 3.5
    location_boundary = ()

    intervention = False

    survey_dates = {
        'bcpp-year-1': SurveyDatesTuple(
            name='bhs',
            start_date=date(2013, 10, 18),
            full_enrollment_date=date(2014, 12, 20),
            end_date=date(2014, 12, 19),
            smc_start_date=date(2015, 11, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2014, 11, 21),
            full_enrollment_date=date(2014, 12, 17),
            end_date=date(2014, 12, 22),
            smc_start_date=date(2014, 12, 22)),
    }

    clinic_days = {
        'bcpp-year-1': {
            'IDCC': ClinicDaysTuple((MO, WE), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-1'].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, WE), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(TestPlotMapper)
