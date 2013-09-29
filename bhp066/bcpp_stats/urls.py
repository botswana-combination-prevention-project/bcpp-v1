from django.conf.urls import patterns, url

urlpatterns = patterns('bhp_model_describer.views',
    url(r'^model_describer/', 'model_describer', name="describer_url_name"),
    )
