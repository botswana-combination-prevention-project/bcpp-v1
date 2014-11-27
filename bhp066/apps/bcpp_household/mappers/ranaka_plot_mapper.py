from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, RANAKA_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


class RanakaPlotMapper(BasePlotMapper):

    map_area = 'ranaka'
    map_code = '11'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = RANAKA_LANDMARKS

    intervention = False

    gps_center_lat = -24.908703
    gps_center_lon = 25.463033
    radius = 4
    location_boundary = ()

    survey_dates = {
        'bcpp-year-1': SurveyDatesTuple(
            name='bhs',
            start_date=date(2013, 10, 18),
            full_enrollment_date=date(2013, 11, 7),
            end_date=date(2013, 11, 22),
            smc_start_date=date(2013, 11, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2014, 10, 18),
            full_enrollment_date=date(2014, 11, 7),
            end_date=date(2014, 11, 22),
            smc_start_date=date(2014, 11, 7)),
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

site_mappers.register(RanakaPlotMapper)
