from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, SEFOPHE_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


class SefophePlotMapper(BasePlotMapper):

    map_area = 'sefophe'
    map_code = '22'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = SEFOPHE_LANDMARKS

    intervention = False

    gps_center_lat = -22.190544
    gps_center_lon = 27.963424
    radius = 5.5
    location_boundary = ()

    survey_dates = {
        'bcpp-year-1': SurveyDatesTuple(
            name='bhs',
            start_date=date(2014, 10, 18),
            full_enrollment_date=date(2014, 12, 19),
            end_date=date(2014, 12, 19),
            smc_start_date=date(2015, 11, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2015, 11, 21),
            full_enrollment_date=date(2015, 12, 17),
            end_date=date(2015, 12, 22),
            smc_start_date=date(2015, 12, 22)),
    }

    clinic_days = {
        'bcpp-year-1': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-1'].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
    }

site_mappers.register(SefophePlotMapper)
