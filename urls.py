from django.conf.urls.defaults import patterns


urlpatterns = patterns('bhp_map.views',
    (r'^add_cart/(?P<mapper_name>\w+)/', 'add_to_cart'),
    (r'^update_cart/(?P<mapper_name>\w+)/', 'update_cart'),
    (r'^empty_cart/(?P<mapper_name>\w+)/', 'empty_cart'),
    (r'^checkout/(?P<mapper_name>\w+)/', 'checkout_cart'),
    (r'^complete/(?P<mapper_name>\w+)/', 'save_cart'),
    (r'^view/(?P<mapper_name>\w+)/', 'plot_item_points'),
    (r'^set_section/(?P<mapper_name>\w+)/', 'set_section'),
    (r'^sections/(?P<mapper_name>\w+)/', 'save_section'),
    (r'^clear_section/(?P<mapper_name>\w+)/', 'clear_section'),
    (r'^clear_all_sections/(?P<mapper_name>\w+)/', 'clear_all_sections'),
    (r'subject_map/(?P<mapper_name>\w+)/', 'subject_map'),
    (r'^upload_household_map/(?P<mapper_name>\w+)/', 'upload_household_map'),
    (r'^map_section/(?P<mapper_name>\w+)/', 'map_section'),
    (r'^db_update/(?P<mapper_name>\w+)/', 'db_update'),
    (r'^gps_point_update/(?P<mapper_name>\w+)/', 'db_update_index'),
    (r'^', 'index/(?P<mapper_name>\w+)/'),
)
