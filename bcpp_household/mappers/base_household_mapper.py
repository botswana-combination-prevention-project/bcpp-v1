from edc_core.bhp_map.classes import Mapper
from edc_core.bhp_map.choices import ICONS, OTHER_ICONS
from bcpp_household.models import Plot


class BaseHouseholdMapper(Mapper):

    item_model = Plot
    item_model_cls = Plot
    item_label = 'Plot'

    region_field_attr = 'section'
    region_label = 'Section'
    section_field_attr = 'sub_section'
    section_label = 'Sub Section'
    map_area_field_attr = 'community'
    target_gps_lat_field_attr = 'gps_target_lat'
    target_gps_lon_field_attr = 'gps_target_lon'
    icons = ICONS
    other_icons = OTHER_ICONS

    identifier_field_attr = 'plot_identifier'
    identifier_field_label = 'plot'
    other_identifier_field_attr = 'cso_number'
    other_identifier_field_label = 'cso'

    item_target_field = 'target'

    gps_degrees_s_field_attr = 'gps_degrees_s'
    gps_degrees_e_field_attr = 'gps_degrees_e'
    gps_minutes_s_field_attr = 'gps_minutes_s'
    gps_minutes_e_field_attr = 'gps_minutes_e'
