from django.conf.urls.defaults import *

urlpatterns = patterns('bhp_nmap.views',
    url(r'^uphosts/', 
        'uphosts', 
        name="uphosts_url_name"
        ),   
    ) 

