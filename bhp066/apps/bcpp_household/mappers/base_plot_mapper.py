from edc.map.classes import Mapper
from edc.map.choices import ICONS, OTHER_ICONS
from apps.bcpp_household.models import Plot


class BasePlotMapper(Mapper):

    item_model = Plot
    item_model_cls = Plot
    item_label = 'Plot'

    region_field_attr = 'section'
    region_label = 'Section'
    section_field_attr = 'sub_section'
    section_label = 'Sub Section'
    map_area_field_attr = 'community'

    #Different map fields, the numbers are the zoom levels
    map_field_attr_18 = 'uploaded_map_18'
    map_field_attr_17 = 'uploaded_map_17'
    map_field_attr_16 = 'uploaded_map_16'

    target_gps_lat_field_attr = 'gps_target_lat'
    target_gps_lon_field_attr = 'gps_target_lon'
    icons = ICONS
    other_icons = OTHER_ICONS

    identifier_field_attr = 'plot_identifier'
    identifier_field_label = 'plot'
    other_identifier_field_attr = 'cso_number'
    other_identifier_field_label = 'cso'

    item_target_field = 'target'
    item_selected_field = 'selected'

    gps_degrees_s_field_attr = 'gps_degrees_s'
    gps_degrees_e_field_attr = 'gps_degrees_e'
    gps_minutes_s_field_attr = 'gps_minutes_s'
    gps_minutes_e_field_attr = 'gps_minutes_e'

    @property
    def test_location(self):
        """Decimal Degrees = Degrees + minutes/60 + seconds/3600"""
        degrees_e, minutes_e = self.deg_to_dms(self.gps_center_lon)
        degrees_s, minutes_s = self.deg_to_dms(self.gps_center_lat)
        return (degrees_s, minutes_s, degrees_e, minutes_e)
