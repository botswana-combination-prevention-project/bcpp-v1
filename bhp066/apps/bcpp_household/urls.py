from django.conf.urls import patterns, url

urlpatterns = patterns('apps.bcpp_household.views',
    url(r'^return/(?P<household>[A-Z0-9\-0-9]+)/', 'return_households')
    )
