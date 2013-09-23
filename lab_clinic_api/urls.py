from django.conf.urls import patterns, url

urlpatterns = patterns('lab_clinic_api.views',
    url(r'^viewresult/(?P<result_identifier>[0-9\-]+)/$',
        'view_result',
        name="view_result_report"
        ),
   )
