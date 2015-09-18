from dateutil.relativedelta import MO, TU, WE, TH, FR, relativedelta
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, DIGAWANA_LANDMARKS


class TestPlotMapper(BasePlotMapper):

    map_area = 'test_community'
    map_code = '01'
    pair = 0
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = DIGAWANA_LANDMARKS

    gps_center_lat = -25.330451
    gps_center_lon = 25.556502
    radius = 3.5
    location_boundary = ()

    intervention = False

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 11, 5),
            full_enrollment_date=date(2015, 11, 28),
            end_date=date(2015, 12, 20),
            smc_start_date=date(2014, 12, 1)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 4, 18),
            full_enrollment_date=date(2015, 4, 30),
            end_date=date(2015, 10, 30),
            smc_start_date=date(2015, 5, 30)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, WE), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, WE), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(TestPlotMapper)
