from django.conf.urls import patterns, url
from .views import correct_consent_form, correct_data_index, increase_plot_radius, consent_form_index, update_radius

urlpatterns = patterns(
    '',
    url(r'^correct_data_index/', correct_data_index, name='correct_data_index_url'),
    url(r'^correct_consent_form/', correct_consent_form, name='correct_consent_form_url'),
    url(r'^consent_form_index/', consent_form_index, name='consent_form_index_url'),
    url(r'^increase_plot_radius/', increase_plot_radius, name='increase_plot_radius_url'),
    url(r'^update_radius/', update_radius, name='update_radius_url'),
)
