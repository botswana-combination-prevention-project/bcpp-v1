from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, GWETA_LANDMARKS


class GwetaPlotMapper(BasePlotMapper):

    map_area = 'gweta'
    map_code = '34'
    pair = 7
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = GWETA_LANDMARKS

    intervention = True

    gps_center_lat = -20.205621
    gps_center_lon = 25.251474
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',

            start_date=date(2015, 7, 7),
            full_enrollment_date=date(2015, 8, 4),
            end_date=date(2015, 8, 25),
            smc_start_date=date(2015, 9, 6)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 21),
            full_enrollment_date=date(2015, 12, 17),
            end_date=date(2015, 12, 22),
            smc_start_date=date(2015, 12, 22)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=None,
            full_enrollment_date=None,
            end_date=None,
            smc_start_date=None),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((TH, ), None),

            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(GwetaPlotMapper)
