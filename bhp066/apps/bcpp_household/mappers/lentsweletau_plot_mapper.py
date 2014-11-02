from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from django.conf import settings

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LENTSWELETAU_LANDMARKS

from ..utils import ClinicDaysTuple


class LentsweletauPlotMapper(BasePlotMapper):

    map_area = 'lentsweletau'
    map_code = '16'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = LENTSWELETAU_LANDMARKS

    gps_center_lat = -24.252443
    gps_center_lon = 25.854249
    radius = 5.0
    location_boundary = ()

    intervention = True
    survey_dates = {'bcpp-year-1': dict(
        bhs_start_date=date(2014, 9, 5),
        bhs_full_enrollment_date=date(2014, 10, 15),
        bhs_end_date=date(2014, 10, 21),
        smc_start_date=date(2014, 10, 27)),
    }
    clinic_days = {'bcpp-year-1': {
        'IDCC': ClinicDaysTuple((MO, WE), None),
        'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), survey_dates['bcpp-year-1'].get('smc_start_date'))
        }
    }

site_mappers.register(LentsweletauPlotMapper)
