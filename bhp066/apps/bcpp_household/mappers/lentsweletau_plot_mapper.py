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
#     clinic_days = {
#         'IDCC': ClinicDaysTuple((MO, WE), None),
#         'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
#         'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
#         'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), settings.SMC_START_DATE)}

site_mappers.register(LentsweletauPlotMapper)
