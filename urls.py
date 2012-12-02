from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('bhp_dispatch.views',
    url(r'^return/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_items',),
    )
