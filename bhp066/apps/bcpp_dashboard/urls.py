from django.conf.urls import patterns, url

from apps.bcpp_dashboard.classes import SubjectDashboard, HouseholdDashboard

regex = {}
regex['dashboard_type'] = 'subject'
regex['dashboard_model'] = 'household_member'
urlpatterns = SubjectDashboard.get_urlpatterns('apps.bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])

regex = {}
regex['dashboard_type'] = 'household'
regex['dashboard_model'] = 'household|household_structure'
urlpatterns += HouseholdDashboard.get_urlpatterns('apps.bcpp_dashboard.views', regex)

urlpatterns += patterns('apps.bcpp_dashboard.views',
    url(r'participation/', 'participation', name='participation_url'))
