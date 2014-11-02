from datetime import date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from django.conf import settings

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, LETLHAKENG_LANDMARKS
from ..utils import ClinicDaysTuple


class LetlhakengPlotMapper(BasePlotMapper):

    map_area = 'letlhakeng'
    map_code = '15'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = LETLHAKENG_LANDMARKS

    gps_center_lat = -24.099361
    gps_center_lon = 25.032163
    radius = 5.0
    location_boundary = ()

    intervention = False
    survey_dates = {'bcpp-year-1': dict(
        bhs_start_date=date(2014, 9, 5),
        bhs_full_enrollment_date=date(2014, 10, 15),
        bhs_end_date=date(2014, 10, 21),
        smc_start_date=date(2014, 10, 29))
    }
    clinic_days = {'bcpp-year-1': {
        'IDCC': ClinicDaysTuple((TU, TH), None),
        'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
        'SMC': ClinicDaysTuple((WE, ), survey_dates['bcpp-year-1'].get('smc_start_date'))
        }
    }

site_mappers.register(LetlhakengPlotMapper)
