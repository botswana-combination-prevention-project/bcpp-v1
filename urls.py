from django.conf.urls.defaults import patterns, include, url
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('audit_trail.views',
    url(r'^(?P<section_name>\w+)/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<dashboard_type>\w+)/(?P<audit_subject_identifier>[\w\-]+)/(?P<audit_id>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<visit_code>\w+)/(?P<visit_instance>\w+)/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^(?P<section_name>\w+)/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<audit_subject_identifier>[\w\-]+)/(?P<audit_id>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^(?P<section_name>\w+)/(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<audit_subject_identifier>[\w\-]+)/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),    
    url(r'^(?P<section_name>\w+)/(?P<app_label>\w+)/(?P<model_name>\w+)/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^(?P<section_name>\w+)/(?P<app_label>\w+)/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^(?P<section_name>\w+)/',
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^',
    'audit_trail_view', 
    name="audit_trail_url"
    ),
)

