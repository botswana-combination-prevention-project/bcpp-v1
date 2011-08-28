from django.conf.urls.defaults import patterns, include, url
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('audit_trail.views',
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^(?P<app_label>\w+)/$', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    url(r'^', 
    'audit_trail_view', 
    name="audit_trail_url"
    ),
    
)

