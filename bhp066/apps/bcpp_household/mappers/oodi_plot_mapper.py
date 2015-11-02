from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, OODI_LANDMARKS


class OodiPlotMapper(BasePlotMapper):

    map_area = 'oodi'
    map_code = '18'
    pair = 4
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = OODI_LANDMARKS

    intervention = True

    gps_center_lat = -24.425856
    gps_center_lon = 26.021626
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 11, 21),
            full_enrollment_date=date(2014, 12, 19),
            end_date=date(2014, 12, 19),
            smc_start_date=date(2014, 12, 1)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 9),
            full_enrollment_date=date(2015, 11, 29),
            end_date=date(2015, 11, 29),
            smc_start_date=date(2015, 12, 1)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(OodiPlotMapper)
