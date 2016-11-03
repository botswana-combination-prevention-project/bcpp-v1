from django.conf.urls import patterns, url
from .views import check_replacements, replace_household_plot, replacement_index, create_plot_log

urlpatterns = patterns(
    '',
    url(r'replacement_index/', replacement_index, name='replacement_index_url'),
    url(r'^return/(?P<household>[A-Z0-9\-0-9]+)/', 'return_households'),
    url(r'^create_plot_log/', create_plot_log, name='create_plot_log_url'),
    url(r'^check_replacements/', check_replacements, name='check_replacements_url'),
    url(r'^replace_household_plot/', replace_household_plot, name='replace_household_plot_url'))
