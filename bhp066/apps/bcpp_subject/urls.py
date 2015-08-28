

from django.conf.urls import patterns, url
from .views import GenerateConfirmationKeyView

urlpatterns = patterns(
    '',
    url(r'^confirmation_code/', GenerateConfirmationKeyView.as_view(), name='generate_confirmation_code_url'),
    )
