from django.db import models
from bhp_sync.models import BaseSyncUuidModel
from bhp_registration.models import RegisteredSubject
from bhp_consent.managers import BaseConsentHistoryManager


class BaseConsentHistory(BaseSyncUuidModel):

    """A base class for the consent history.

    Ties in with the consent model method :func:get_consent_history_model`, the manager method above
    and a signal in :mod:`bhp_consent.models.signals`"""

    registered_subject = models.ForeignKey(RegisteredSubject)
    consent_datetime = models.DateTimeField()
    consent_pk = models.CharField(max_length=50)
    consent_app_label = models.CharField(max_length=50)
    consent_model_name = models.CharField(max_length=50)

    objects = BaseConsentHistoryManager()

    class Meta:
        abstract = True
