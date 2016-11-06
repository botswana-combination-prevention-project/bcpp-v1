from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc_map.site_mappers import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, NATA_LANDMARKS


class NataPlotMapper(BasePlotMapper):

    map_area = 'nata'
    map_code = '38'
    pair = 15
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = NATA_LANDMARKS

    intervention = False

    gps_center_lat = -20.207917
    gps_center_lon = 26.184711
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2015, 10, 15),
            full_enrollment_date=date(2015, 11, 30),
            end_date=date(2015, 11, 30),
            smc_start_date=date(2016, 1, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2016, 10, 22),
            full_enrollment_date=date(2016, 11, 28),
            end_date=date(2016, 11, 29),
            smc_start_date=date(2016, 11, 22)),
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
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(NataPlotMapper)
