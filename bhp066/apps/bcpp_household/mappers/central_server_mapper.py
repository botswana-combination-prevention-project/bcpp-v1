from edc.map.classes import site_mappers

from .base_plot_mapper import BasePlotMapper


class CentralServerMapper(BasePlotMapper):
    """A special mapper for the central server only that
    allows survey and plot checks to be bypassed in
    most cases, e.g. at boot up."""

    map_area = 'bhp'  # corresponds with settings.CURRENT_COMMUNITY
    map_code = '00'  # corresponds with settings.SITE_CODE
    regions = ()
    sections = ()

    landmarks = ()

    intervention = None

    gps_center_lat = 0
    gps_center_lon = 0
    radius = 0
    location_boundary = ()

    survey_dates = {}

    clinic_days = {}

site_mappers.register(CentralServerMapper)
