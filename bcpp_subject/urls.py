from django.conf.urls import url, patterns

from edc_quota.override.views import OverrideCodeView

urlpatterns = patterns(
    '',
    url(r'^override_code/',
        OverrideCodeView.as_view(template_name='override_code_bcpp.html'),
        name='override_code_url_bcpp'),
)
