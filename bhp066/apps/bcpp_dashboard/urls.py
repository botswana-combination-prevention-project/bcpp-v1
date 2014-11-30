from django.conf.urls import patterns, url

from apps.bcpp_dashboard.classes import SubjectDashboard, HouseholdDashboard, ClinicDashboard
from django.contrib.auth.decorators import login_required



# regex = {}
# regex['dashboard_type'] = 'subject'
# regex['dashboard_model'] = 'household_member'
# urlpatterns = SubjectDashboard.get_urlpatterns('apps.bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])
# urlpatterns = SubjectDashboard.get_urlpatterns(visit_field_names=['subject_visit', ])

# regex = {}
# regex['dashboard_type'] = 'household'
# regex['dashboard_model'] = 'household|household_structure'
# urlpatterns += HouseholdDashboard.get_urlpatterns()
urlpatterns = []
for pattern in HouseholdDashboard.get_urlpatterns():
    urlpatterns.append(url(pattern, HouseholdDashboard.as_view(), name=HouseholdDashboard.dashboard_url_name))
for pattern in SubjectDashboard.get_urlpatterns():
    urlpatterns.append(url(pattern, SubjectDashboard.as_view(), name=SubjectDashboard.dashboard_url_name))

urlpatterns += patterns('apps.bcpp_dashboard.views',
    url(r'participation/', 'participation', name='participation_url'))

# regex = {}
# regex['dashboard_type'] = 'clinic'
# regex['dashboard_model'] = 'clinic_eligibility'
# urlpatterns += ClinicDashboard.get_urlpatterns('apps.bcpp_dashboard.views', regex, visit_field_names=['clinic_visit', ])
