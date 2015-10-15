from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MASUNGA_LANDMARKS


class MasungaPlotMapper(BasePlotMapper):

    map_area = 'masunga'
    map_code = '37'
    pair = 15
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MASUNGA_LANDMARKS

    intervention = True

    gps_center_lat = -20.667218
    gps_center_lon = 27.428340
    radius = 6.0
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 10, 15),
            full_enrollment_date=date(2015, 11, 7),
            end_date=date(2015, 11, 14),
            smc_start_date=date(2016, 1, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2016, 1, 1),
            full_enrollment_date=date(2016, 2, 17),
            end_date=date(2016, 2, 22),
            smc_start_date=date(2016, 12, 22)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(MasungaPlotMapper)
