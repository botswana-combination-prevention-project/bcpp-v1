from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
import databrowse
from django.db.models import get_models
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bhp_entry_rules.classes import rule_groups
from bhp_search.classes import search
from dajaxice.core import dajaxice_autodiscover
from bhp_lab_tracker.classes import lab_tracker
from bhp_site_edc import edc

admin.autodiscover()
dajaxice_autodiscover()
rule_groups.autodiscover()
lab_tracker.autodiscover()
search.autodiscover()

for model in get_models():
    databrowse.site.register(model)

urlpatterns = staticfiles_urlpatterns()

app_name = settings.APP_NAME

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', redirect_to, {'url': '/{app_name}/logout/'.format(app_name=app_name)}),
    (r'^admin/login/$', redirect_to, {'url': '/{app_name}/login/'.format(app_name=app_name)}),
    (r'^admin/passwordchange/$', redirect_to, {'url': '/{app_name}/passwordchange/'.format(app_name=app_name)}),
    (r'^admin/passwordchangedone/$', redirect_to, {'url': '/{app_name}/passwordchangedone/'.format(app_name=app_name)}),
    (r'^admin/', include(admin.site.urls)),
    (r'^edc/', include(edc.site.urls)),

)

urlpatterns += patterns('',
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

urlpatterns += patterns('',
    (r'^databrowse/(.*)', login_required(databrowse.site.root)),
)

urlpatterns += patterns('',
    (r'^audit_trail/', include('audit_trail.urls')),
    (r'^{app_name}/audit_trail/'.format(app_name=app_name), include('audit_trail.urls')),
    (r'^bhp_sync/', include('bhp_sync.urls')),
)

urlpatterns += patterns('',
    url(r'^{app_name}/(?P<section_name>statistics)/'.format(app_name=app_name), include('{app_name}_stats.urls'.format(app_name=app_name)), name="section_url_name"),
)

urlpatterns += patterns('',
    url(r'^{app_name}/(?P<section_name>lab)/'.format(app_name=app_name), include('lab_clinic_api.urls'), name="section_url_name"),
)


urlpatterns += patterns('',
    url(r'^{app_name}/dashboard/'.format(app_name=app_name), include('{app_name}_dashboard.urls'.format(app_name=app_name))),
)

urlpatterns += patterns('',
    url(r'^{app_name}/login/'.format(app_name=app_name), 'django.contrib.auth.views.login', name='{app_name}_login'.format(app_name=app_name)),
    url(r'^{app_name}/logout/'.format(app_name=app_name), 'django.contrib.auth.views.logout_then_login', name='{app_name}_logout'.format(app_name=app_name)),
    url(r'^{app_name}/passwordchange/'.format(app_name=app_name), 'django.contrib.auth.views.password_change', name='{app_name}_password_change'.format(app_name=app_name)),
    url(r'^{app_name}/passwordchangedone/'.format(app_name=app_name), 'django.contrib.auth.views.password_change_done', name='{app_name}_password_change_done'.format(app_name=app_name)),
    #url(r'^{app_name}/section/search/'.format(app_name=app_name), include('bhp_search.urls'), name='search'),
    url(r'^{app_name}/section/'.format(app_name=app_name), include('bhp_section.urls'), name='section'),

    url(r'^{app_name}/'.format(app_name=app_name), redirect_to, {'url': '/{app_name}/section/'.format(app_name=app_name)}),

)
