from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MMATHETHE_LANDMARKS


class MmathethePlotMapper(BasePlotMapper):

    map_area = 'mmathethe'
    map_code = '20'
    pair = 5
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MMATHETHE_LANDMARKS

    intervention = False

    gps_center_lat = -25.320035
    gps_center_lon = 25.266402
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 1, 19),
            full_enrollment_date=date(2015, 2, 10),
            end_date=date(2015, 3, 3),
            smc_start_date=date(2015, 2, 13)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 21),
            full_enrollment_date=date(2015, 12, 17),
            end_date=date(2015, 12, 22),
            smc_start_date=date(2015, 12, 22)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=date(2015, 12, 4),
            full_enrollment_date=date(2016, 1, 31),
            end_date=date(2016, 1, 31),
            smc_start_date=date(2016, 1, 31)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((TU, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((TU, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
        'bcpp-year-3': {
            'IDCC': ClinicDaysTuple((TU, TH, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-3'].smc_start_date)},
    }

site_mappers.register(MmathethePlotMapper)
