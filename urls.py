from django.conf.urls.defaults import patterns, url
from bhp_map.classes import mapper


urlpatterns = patterns('bhp_map.views',
    url(r'^add_cart/(?P<mapper_name>\w+)/', 'add_to_cart', name='map_add_cart_url'),
#     url(r'^update_cart/(?P<mapper_name>\w+)/', 'update_cart'),
#     url(r'^empty_cart/(?P<mapper_name>\w+)/', 'empty_cart'),
    url(r'^checkout/(?P<mapper_name>\w+)/', 'checkout_cart', name='map_checkout_cart_url'),
#     url(r'^complete/(?P<mapper_name>\w+)/', 'save_cart'),
    url(r'^view/(?P<mapper_name>\w+)/', 'plot_item_points', name='map_plot_item_points_url'),
    url(r'^set_section/(?P<mapper_name>\w+)/', 'set_section', name='set_section_url'),
#     url(r'^sections/(?P<mapper_name>\w+)/', 'save_section'),
    url(r'^clear_section/(?P<mapper_name>\w+)/', 'clear_section', name='clear_section_url'),
    url(r'^clear_all_sections/(?P<mapper_name>\w+)/', 'clear_all_sections', name='clear_all_sections_url'),
#     url(r'^subject_map/(?P<mapper_name>\w+)/', 'subject_map'),
#     url(r'^upload_household_map/(?P<mapper_name>\w+)/', 'upload_household_map'),
    url(r'^map_section/(?P<mapper_name>\w+)/', 'map_section', name='map_section_url'),
    url(r'^db_update/(?P<mapper_name>\w+)/', 'db_update', name='map_db_update'),
    url(r'^gps_point_update/(?P<mapper_name>\w+)/', 'db_update_index', name='map_gps_point_update_url'),
)

for mapper_name in mapper.get_registry().iterkeys():
    urlpatterns += patterns('bhp_map.views', url(r'^(?P<mapper_name>{0})/$'.format(mapper_name), 'map_index', name='selected_map_index_url'))

urlpatterns += patterns('bhp_map.views', url(r'^', 'map_index', name='map_index_url'))
