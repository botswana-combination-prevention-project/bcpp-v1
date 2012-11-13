from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('lab_requisition.views',
    url(r'^requisition/(?P<subject_type>\w+)/(?P<requisition_identifier_label>requisition_identifier)/(?P<identifier>\w+)/$',
        'view_requisition',
        name="view_requisition"),
   url(r'^requisition/(?P<subject_type>\w+)/(?P<requisition_identifier_label>specimen_identifier)/(?P<identifier>\w+)/$',
        'view_requisition',
        name="view_requisition"))
