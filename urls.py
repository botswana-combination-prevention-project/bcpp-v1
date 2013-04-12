from django.contrib import admin
from bcpp_dashboard.classes import SubjectDashboard
admin.autodiscover()

regex = {}
regex['dashboard_type'] = 'subject'
regex['subject_identifier'] = '066-[0-9]{9,11}-[0-9]{1}'
regex['visit_code'] = '\w+'
regex['visit_instance'] = '[0-9]{1}'
subject_dashboard = SubjectDashboard()
urlpatterns = subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit'])
# regex['subject_identifier'] = '066-[0-9]{3}-[0-9]{4}'
# urlpatterns += subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])
