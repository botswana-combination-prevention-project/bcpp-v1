from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from ..constants import BASELINE_SURVEY_SLUG
from ..utils import ClinicDaysTuple, SurveyDatesTuple

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, RANAKA_LANDMARKS


class RanakaPlotMapper(BasePlotMapper):

    map_area = 'ranaka'
    map_code = '11'
    pair = 1
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = RANAKA_LANDMARKS

    intervention = False

    gps_center_lat = -24.908703
    gps_center_lon = 25.463033
    radius = 4
    location_boundary = ()

    survey_dates = {
        BASELINE_SURVEY_SLUG: SurveyDatesTuple(
            name='bhs',
            start_date=date(2013, 10, 18),
            full_enrollment_date=date(2013, 11, 7),
            end_date=date(2013, 11, 22),
            smc_start_date=date(2013, 11, 7)),
        'bcpp-year-2': SurveyDatesTuple(
            name='t1',
            start_date=date(2014, 11, 21),  # date we start calling
            full_enrollment_date=date(2015, 1, 18),
            end_date=date(2015, 1, 30),
            # non SMC referrals in ECC? see SubjectReferralHelper
            smc_start_date=date(2015, 1, 7)),
        'bcpp-year-3': SurveyDatesTuple(
            name='t2',
            start_date=date(2015, 12, 4),
            full_enrollment_date=date(2016, 1, 31),
            end_date=date(2016, 1, 31),
            smc_start_date=date(2016, 1, 31)),
    }

    clinic_days = {
        BASELINE_SURVEY_SLUG: {
            'IDCC': ClinicDaysTuple((MO, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates[BASELINE_SURVEY_SLUG].smc_start_date)},
        'bcpp-year-2': {
            'IDCC': ClinicDaysTuple((TU, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-2'].smc_start_date)},
        'bcpp-year-3': {
            'IDCC': ClinicDaysTuple((WE, ), None),
            'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
            'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-3'].smc_start_date)},
    }

site_mappers.register(RanakaPlotMapper)
