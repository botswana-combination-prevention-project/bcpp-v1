from django.conf.urls.defaults import *

urlpatterns = patterns('bhp_common.views',
    (r'^issuetracker/$', 'issue_tracker_search'),            
) 
