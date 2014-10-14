from django.conf.urls import patterns, url

from .classes import ClinicDashboard

regex = {}
regex['dashboard_type'] = 'subject'
regex['dashboard_model'] = 'clinic_consent'
urlpatterns = ClinicDashboard.get_urlpatterns('apps.bcpp_clinic_dashboard.views', regex, visit_field_names=['clinic_visit', ])

# regex = {}
# regex['dashboard_type'] = 'subject'
# regex['dashboard_model'] = 'household_member'
# urlpatterns = SubjectDashboard.get_urlpatterns('apps.bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])