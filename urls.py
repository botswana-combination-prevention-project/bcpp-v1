from django.conf.urls.defaults import *

urlpatterns = patterns('bhp_visit.views',
    (r'^scheduled_forms/$', 'scheduled_forms'),            
) 
