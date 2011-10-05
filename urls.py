from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('lab_clinic_api.views',
    url(r'^viewresult/(?P<result_identifier>[0-9\-]+)/$', 
        'view_result', 
        name="lab_clinic_api_result_report"
        ),

    url(r'^charts/(?P<subject_identifier>[0-9A-Z\-]+)/(?P<test_code>\w+)/chart.png$', 'longitudinal_result'),    

    url(r'^', 
        'index', 
        name="lab_clinic_api_index_url"
        ),
        
    )        
