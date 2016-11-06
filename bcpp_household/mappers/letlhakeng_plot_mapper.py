from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from edc_map.site_mappers import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LETLHAKENG_LANDMARKS


class LetlhakengPlotMapper(BasePlotMapper):

    map_area = 'letlhakeng'
    map_code = '15'
    pair = 3
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = LETLHAKENG_LANDMARKS

    gps_center_lat = -24.099361
    gps_center_lon = 25.032163
    radius = 5.0
    location_boundary = ()

    intervention = False

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 9, 5),
            full_enrollment_date=date(2014, 10, 15),
            end_date=date(2014, 10, 21),
            smc_start_date=date(2014, 10, 29)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 9, 18),
            full_enrollment_date=date(2015, 10, 15),
            end_date=date(2015, 12, 1),
            smc_start_date=date(2015, 10, 29)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((TU, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((WE, ), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((TU, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((WE, ), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(LetlhakengPlotMapper)
