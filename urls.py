from django.conf.urls.defaults import patterns


urlpatterns = patterns('bhp_mapping.views',
    (r'^add_cart/', 'add_to_cart'),
    (r'^update_cart/', 'update_cart'),
    (r'^empty_cart/', 'empty_cart'),
    (r'^checkout/', 'checkout_cart'),
    (r'^complete/', 'save_cart'),
    (r'^view/', 'plot_item_points'),
    (r'^set_section/', 'set_section'),
    (r'^sections/', 'save_section'),
    (r'^clear_section/', 'clear_section'),
    (r'^clear_all_sections/', 'clear_all_sections'),
    (r'subject_map/', 'subject_map'),
    (r'^upload_household_map/', 'upload_household_map'),
    (r'^map_section/', 'map_section'),
    (r'^db_update/', 'db_update'),
    (r'^gps_point_update/', 'db_update_index'),
    (r'^', 'index'),
)
