from django.conf.urls.defaults import url, patterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/$', 
        'data_describer', 
        name="describer_url_name"
        ),
   
    url(r'^counter/', 
        'model_instance_counter', 
        name="model_instance_counter_url_name"
        ),
                       
    url(r'', 
        'data_describer', 
        name="describer_url_name"
        ),                    
    )        


