from django.conf.urls.defaults import patterns, url
#from django.conf import settings
from django.contrib import admin
admin.autodiscover()

#check for LAB_IMPORT_DMIS_DATA_SOURCE in settings
#try:
#    settings.LAB_IMPORT_DMIS_DATA_SOURCE
#except:
#    raise TypeError('module lab_import_dmis requires data source string parameter \'LAB_IMPORT_DMIS_DATA_SOURCE\'. Please add to the settings.py')    


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
