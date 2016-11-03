from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc_map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, METSIMOTLHABE_LANDMARKS


class MetsimotlhabePlotMapper(BasePlotMapper):

    map_area = 'metsimotlhabe'
    map_code = '29'
    pair = 9
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = METSIMOTLHABE_LANDMARKS

    intervention = False

    gps_center_lat = -24.554426
    gps_center_lon = 25.809554
    radius = 7.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 5, 1),
            full_enrollment_date=date(2015, 5, 31),
            end_date=date(2015, 6, 21),
            smc_start_date=date(2015, 8, 10)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2016, 05, 19),
            full_enrollment_date=date(2016, 06, 10),
            end_date=date(2016, 06, 10),
            smc_start_date=date(2016, 06, 10)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, TH, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, TH), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(MetsimotlhabePlotMapper)
