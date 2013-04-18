from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
import databrowse
from django.db.models import get_models
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bhp_entry_rules.classes import rule_groups
from dajaxice.core import dajaxice_autodiscover
from bhp_lab_tracker.classes import lab_tracker


admin.autodiscover()
dajaxice_autodiscover()
rule_groups.autodiscover()
lab_tracker.autodiscover()

for model in get_models():
    databrowse.site.register(model)

urlpatterns = staticfiles_urlpatterns()

urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/logout/$', redirect_to, {'url': '/bcpp/logout/'}),
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
    (r'^bcpp/audit_trail/', include('audit_trail.urls')),
    (r'^bhp_sync/', include('bhp_sync.urls')),
)

urlpatterns += patterns('',
    url(r'^bcpp/(?P<section_name>statistics)/', include('bcpp_stats.urls'), name="section_url_name"),
)

urlpatterns += patterns('',
    url(r'^bcpp/(?P<section_name>specimens)/', include('lab_clinic_api.urls'), name="section_url_name"),
)


urlpatterns += patterns('',
    url(r'^bcpp/dashboard/', include('bcpp_dashboard.urls')),
)

urlpatterns += patterns('',
    url(r'^bcpp/login/', 'django.contrib.auth.views.login', name='bcpp_login'),
    url(r'^bcpp/logout/', 'django.contrib.auth.views.logout_then_login', name='bcpp_logout'),
    url(r'^bcpp/passwordchange/', 'django.contrib.auth.views.password_change', name='bcpp_password_change'),
    url(r'^bcpp/passwordchangedone/', 'django.contrib.auth.views.password_change_done', name='bcpp_password_change_done'),
    url(r'^bcpp/', include('bcpp.urls'), name='home'),
    url(r'', include('bcpp.urls'), name='index'),
)
