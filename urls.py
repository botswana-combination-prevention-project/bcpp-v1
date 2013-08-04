from django.contrib import admin
from django.conf.urls.defaults import patterns, url

from bcpp_dashboard.classes import SubjectDashboard, HouseholdDashboard

admin.autodiscover()

regex = {}
regex['dashboard_type'] = 'subject'
regex['dashboard_model'] = 'household_member'
subject_dashboard = SubjectDashboard()
urlpatterns = subject_dashboard.get_urlpatterns('bcpp_dashboard.views', regex, visit_field_names=['subject_visit', ])

regex = {}
regex['dashboard_type'] = 'household'
regex['household_identifier'] = '[A-Z]{1}[0-9]{6,8}\-[0-9]{2,3}'
household_dashboard = HouseholdDashboard()
urlpatterns += household_dashboard.get_urlpatterns('bcpp_dashboard.views', regex,)

urlpatterns += patterns('bcpp_dashboard.views',
    url(r'participation/', 'participation', name='participation_url'))
