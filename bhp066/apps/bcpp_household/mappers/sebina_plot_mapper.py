from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, SEBINA_LANDMARKS


class SebinaPlotMapper(BasePlotMapper):

    map_area = 'sebina'
    map_code = '28'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = SEBINA_LANDMARKS

    intervention = False

    gps_center_lat = -20.806103
    gps_center_lon = 27.200003
    radius = 6.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 6, 1),
            full_enrollment_date=date(2015, 6, 15),
            end_date=date(2015, 7, 6),
            smc_start_date=date(2015, 8, 10)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 21),
            full_enrollment_date=date(2015, 12, 17),
            end_date=date(2015, 12, 22),
            smc_start_date=date(2015, 12, 22)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((WE, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(SebinaPlotMapper)
