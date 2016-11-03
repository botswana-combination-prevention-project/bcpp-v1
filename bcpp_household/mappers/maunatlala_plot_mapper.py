from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc_map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MAUNATLALA_LANDMARKS


class MaunatlalaPlotMapper(BasePlotMapper):

    map_area = 'maunatlala'
    map_code = '23'
    pair = 7
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MAUNATLALA_LANDMARKS

    intervention = True

    gps_center_lat = -22.8658437618
    gps_center_lon = 27.4198811366
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 3, 7),
            full_enrollment_date=date(2015, 3, 25),
            end_date=date(2015, 4, 15),
            smc_start_date=date(2015, 4, 20)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2016, 3, 11),
            full_enrollment_date=date(2016, 4, 25),
            end_date=date(2016, 4, 26),
            smc_start_date=date(2016, 4, 20)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(MaunatlalaPlotMapper)
