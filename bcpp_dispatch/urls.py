from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bcpp_dispatch.views',
    #url(r'^return/(?P<household>[H0-9\-0-9]+)/', 'return_households'),
    url(r'^', 'bcpp_dispatch',),
    )
