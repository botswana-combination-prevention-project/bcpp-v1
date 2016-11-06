from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc_map.site_mappers import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, SHOSHONG_LANDMARKS


class ShoshongPlotMapper(BasePlotMapper):

    map_area = 'shoshong'
    map_code = '25'
    pair = 8
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = SHOSHONG_LANDMARKS

    intervention = True

    gps_center_lat = -23.032546
    gps_center_lon = 26.516352
    radius = 6.0
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
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((TU, WE, TH, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(ShoshongPlotMapper)
