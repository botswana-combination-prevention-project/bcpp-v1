from django.conf.urls import patterns, url

urlpatterns = patterns('bhp_nmap.views',
    url(r'^uphosts/',
        'uphosts',
        name="uphosts_url_name"
        ),
    )
