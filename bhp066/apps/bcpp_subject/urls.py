from django.conf.urls import include, url, patterns
from edc_quota.client.api import QuotaResource
from tastypie.api import Api

from .views import GenerateConfirmationKeyView

urlpatterns = patterns(
    '',
    url(r'^confirmation_code/', GenerateConfirmationKeyView.as_view(), name='generate_confirmation_code_url'),
)
api = Api(api_name='v1')
api.register(QuotaResource())

urlpatterns += [url(r'^api/', include(api.urls))]
