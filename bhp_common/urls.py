from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bhp_common.views',
    url(r'^', 'show_url_patterns'))
