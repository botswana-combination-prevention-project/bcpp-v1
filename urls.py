from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('lab_barcode.views',
    url(r'', "simple_labeller", name="simple_label_name"), 
    )        

