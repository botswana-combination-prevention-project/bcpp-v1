from bhp_map.classes import mapper
from base_household_mapper import BaseHouseholdMapper
from bcpp_household.choices import OTSE_WARDS, OTSE_WARD_SECTIONS, OTSE_LANDMARKS


class OtseHouseholdMapper(BaseHouseholdMapper):

    map_area = 'otse'

    regions = OTSE_WARDS
    sections = OTSE_WARD_SECTIONS

    landmarks = OTSE_LANDMARKS

    identifier_field_attr = 'household_identifier'
    identifier_field_label = 'household'
    other_identifier_field_attr = 'cso_number'
    other_identifier_field_label = 'cso'

    gps_center_lat = -24.376534
    gps_center_lon = 26.152276
    gps_radius = 8.699197

mapper.register(OtseHouseholdMapper)
