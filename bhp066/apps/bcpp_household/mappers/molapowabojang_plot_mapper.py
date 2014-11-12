from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import date

from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper
from .choices import SECTIONS, SUB_SECTIONS, MOLAPOWABOJANG_LANDMARKS

from ..utils import ClinicDaysTuple, SurveyDatesTuple


class MolapowabojangPlotMapper(BasePlotMapper):

    map_area = 'molapowabojang'
    map_code = '13'
    regions = SECTIONS
    sections = SUB_SECTIONS

    landmarks = MOLAPOWABOJANG_LANDMARKS

    intervention = False

    gps_center_lat = -25.204009
    gps_center_lon = 25.562754
    radius = 5.5
    location_boundary = ()

site_mappers.register(MolapowabojangPlotMapper)
