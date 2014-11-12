from .classes import ClinicDashboard

regex = {}
regex['dashboard_type'] = 'clinic'
regex['dashboard_model'] = 'clinic_eligibility'
urlpatterns = ClinicDashboard.get_urlpatterns('apps.bcpp_clinic_dashboard.views', regex, visit_field_names=['clinic_visit', ])
