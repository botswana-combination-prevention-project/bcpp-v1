import databrowse
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required
from django.db.models import get_models
from django import get_version
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover
from bhp_entry_rules.classes import rule_groups
from bhp_lab_tracker.classes import lab_tracker
from lab_requisition.classes import requisitions

APP_NAME = settings.APP_NAME

admin.autodiscover()
dajaxice_autodiscover()
rule_groups.autodiscover()
lab_tracker.autodiscover()
requisitions.autodiscover()

if not get_version() == '1.4':
    raise ValueError('Incorrect django version. '
                     'Must be 1.4. Got {0}'.format(get_version()))
for model in get_models():
    databrowse.site.register(model)
urlpatterns = staticfiles_urlpatterns()

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', redirect_to, {'url': '/{app_name}/logout/'.format(app_name=APP_NAME)}),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

urlpatterns += patterns('',
    (r'^databrowse/(.*)', login_required(databrowse.site.root)),
)

urlpatterns += patterns('',
    (r'^audit_trail/', include('audit_trail.urls')),
    (r'^{app_name}/audit_trail/'.format(app_name=APP_NAME), include('audit_trail.urls')),
    (r'^bhp_sync/', include('bhp_sync.urls')),
)

urlpatterns += patterns('',
    url(r'^{app_name}/(?P<section_name>specimens)/'.format(app_name=APP_NAME),
        include('lab_clinic_api.urls')),
)

urlpatterns += patterns('bhp_model_describer.views',
    url(r'^{app_name}/(?P<section_name>statistics)/model_describer/(?P<common_foreign_key_field_name>registered_subject|patient_visit)/$'.format(app_name=APP_NAME), 'model_group_describer', name="model_group_describer_url_name"),
    )

urlpatterns += patterns('bhp_model_describer.views',
    url(r'^{app_name}/(?P<section_name>statistics)/model_describer/counter/'.format(app_name=APP_NAME), 'model_instance_counter', name="model_instance_counter_url_name"),
    )

urlpatterns += patterns('bhp_model_describer.views',
    url(r'^{app_name}/(?P<section_name>statistics)/model_describer/'.format(app_name=APP_NAME), 'model_describer', name="model_describer_url_name"),
    )
urlpatterns += patterns('',
    url(r'^{app_name}/(?P<section_name>specimens)/'.format(app_name=APP_NAME), include('lab_clinic_api.urls'), name="section_url_name"),
)

urlpatterns += patterns('',
    url(r'^{app_name}/dashboard/'.format(app_name=APP_NAME),
        include('{app_name}_dashboard.urls'.format(app_name=APP_NAME))),
)

urlpatterns += patterns('',
    url(r'^{app_name}/login/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.login',
        name='{app_name}_login'.format(app_name=APP_NAME)),
    url(r'^{app_name}/logout/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.logout_then_login',
        name='{app_name}_logout'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change',
        name='password_change_url'.format(app_name=APP_NAME)),
    url(r'^{app_name}/password_change_done/'.format(app_name=APP_NAME),
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'.format(app_name=APP_NAME)),
)

urlpatterns += patterns('',
    url(r'^{app_name}/'.format(app_name=APP_NAME),
        include('{app_name}.urls'.format(app_name=APP_NAME)), name='home'),
    url(r'', redirect_to, {'url': '/{app_name}/'.format(app_name=APP_NAME)}),
    )
