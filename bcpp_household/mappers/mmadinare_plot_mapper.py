from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc_map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MMADINARE_LANDMARKS


class MmadinarePlotMapper(BasePlotMapper):

    map_area = 'mmadinare'
    map_code = '26'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MMADINARE_LANDMARKS

    intervention = False

    gps_center_lat = -21.869753
    gps_center_lon = 27.753179
    radius = 7.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 3, 27),
            full_enrollment_date=date(2015, 4, 24),
            end_date=date(2015, 5, 8),
            smc_start_date=date(2015, 5, 11)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2016, 3, 31),
            full_enrollment_date=date(2016, 4, 20),
            end_date=date(2016, 4, 22),
            smc_start_date=date(2016, 4, 22)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, TU, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(MmadinarePlotMapper)
