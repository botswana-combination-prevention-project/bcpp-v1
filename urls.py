from django.contrib import admin
from django.conf.urls.defaults import patterns, url

from bcpp_dashboard.classes import SubjectDashboard, HouseholdDashboard

admin.autodiscover()

regex = {}
regex['dashboard_type'] = 'subject'
regex['subject_identifier'] = 'S[0-9]{6}\-[0-9]{2}\-[A-Z]{3}[0-9]{2}'
regex['visit_code'] = '[A-Z0-9]+'
regex['visit_instance'] = '[0-9]{1}'
subject_dashboard = SubjectDashboard()
urlpatterns = subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])

regex = {}
regex['dashboard_type'] = 'subject'
regex['subject_identifier'] = 'S[0-9]{3}\-[0-9]{3}'
regex['visit_code'] = '[A-Z0-9]+'
regex['visit_instance'] = '[0-9]{1}'
subject_dashboard = SubjectDashboard()
urlpatterns += subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])

regex = {}
regex['dashboard_type'] = 'subject'
regex['subject_identifier'] = '066\-[0-9]{6,8}\-[0-9]{1}'
regex['visit_code'] = '[A-Z0-9]+'
regex['visit_instance'] = '[0-9]{1}'
subject_dashboard = SubjectDashboard()
urlpatterns += subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])


regex = {}
regex['dashboard_type'] = 'subject'
regex['subject_identifier'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'
regex['visit_code'] = '[A-Z0-9]+'
regex['visit_instance'] = '[0-9]{1}'
subject_dashboard = SubjectDashboard()
urlpatterns += subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])

regex = {}
regex['dashboard_type'] = 'household'
regex['household_identifier'] = 'H[0-9]{3,6}\-[0-9]{1,3}'
household_dashboard = HouseholdDashboard()
urlpatterns += household_dashboard.get_urlpatterns('bcpp_dashboard.views', regex,)

urlpatterns += patterns('bcpp_dashboard.views',
    url(r'participation/', 'participation',))
