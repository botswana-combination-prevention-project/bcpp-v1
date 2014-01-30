from django.conf.urls import patterns, url

from .classes import ClinicDashboard

regex = {}
regex['dashboard_type'] = 'clinic'
regex['dashboard_model'] = 'clinic_consent'
urlpatterns = ClinicDashboard.get_urlpatterns('apps.bcpp_clinic_dashboard.views', regex, visit_field_names=['clinic_visit', ])
