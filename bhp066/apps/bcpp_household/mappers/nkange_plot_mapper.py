from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, NKANGE_LANDMARKS


class NkangePlotMapper(BasePlotMapper):

    map_area = 'nkange'
    map_code = '27'
    pair = 10
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = NKANGE_LANDMARKS

    intervention = True

    gps_center_lat = -20.29269441
    gps_center_lon = 27.13549895
    radius = 6.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2013, 10, 18),
            full_enrollment_date=date(2013, 11, 7),
            end_date=date(2013, 11, 22),
            smc_start_date=date(2013, 11, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2014, 12, 8),
            full_enrollment_date=date(2015, 1, 18),
            end_date=date(2015, 1, 30),
            smc_start_date=date(2015, 1, 7)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=date(2015, 12, 4),
            full_enrollment_date=date(2016, 1, 31),
            end_date=date(2016, 1, 31),
            smc_start_date=date(2016, 1, 31)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((TU, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(NkangePlotMapper)
