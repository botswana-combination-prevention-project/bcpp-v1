from bhp_map.classes import Mapper
from bcpp_household.models import Household
from bhp_map.classes import mapper
from bhp_map.choices import ICONS, OTHER_ICONS


class BaseHouseholdMapper(Mapper):

    item_model = Household
    item_label = 'Household'

    region_field_attr = 'ward'
    region_label = 'Ward'
    section_field_attr = 'ward_section'
    section_label = 'Ward Section'
    icons = ICONS
    other_icons = OTHER_ICONS

    identifier_field_attr = 'household_identifier'
    identifier_field_label = 'household'
    other_identifier_field_attr = 'cso_number'
    other_identifier_field_label = 'cso'

    item_target_field = 'target'

    gps_e_field_attr = 'gps_point_1'
    gps_s_field_attr = 'gps_point_2'
    gps_latitude_field_attr = 'gps_point_11'
    gps_longitude_field_attr = 'gps_point_21'

mapper.register(BaseHouseholdMapper)
