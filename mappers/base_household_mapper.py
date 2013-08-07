from bhp_map.classes import Mapper
from bcpp_household.models import Household
from bhp_map.choices import ICONS, OTHER_ICONS


class BaseHouseholdMapper(Mapper):

    item_model = Household
    item_model_cls = Household
    item_label = 'Household'

    region_field_attr = 'section'
    region_label = 'Section'
    section_field_attr = 'sub_section'
    section_label = 'Sub Section'
    icons = ICONS
    other_icons = OTHER_ICONS

    identifier_field_attr = 'household_identifier'
    identifier_field_label = 'household'
    other_identifier_field_attr = 'cso_number'
    other_identifier_field_label = 'cso'

    item_target_field = 'target'

    gps_degrees_s_field_attr = 'gps_degrees_s'
    gps_degrees_e_field_attr = 'gps_degrees_e'
    gps_minutes_s_field_attr = 'gps_minutes_s'
    gps_minutes_e_field_attr = 'gps_minutes_e'
