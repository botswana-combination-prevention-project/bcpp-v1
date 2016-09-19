from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc_map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, SEFHARE_LANDMARKS


class SefharePlotMapper(BasePlotMapper):

    map_area = 'sefhare'
    map_code = '39'
    pair = 14
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = SEFHARE_LANDMARKS

    intervention = True

    gps_center_lat = -23.027271
    gps_center_lon = 27.526095
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 9, 9),
            full_enrollment_date=date(2014, 10, 7),
            end_date=date(2014, 10, 28),
            smc_start_date=date(2015, 1, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2016, 9, 23),
            full_enrollment_date=date(2016, 10, 17),
            end_date=date(2016, 10, 17),
            smc_start_date=date(2016, 10, 17)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, TU, TH, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(SefharePlotMapper)
