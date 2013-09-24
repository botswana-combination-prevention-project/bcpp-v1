from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_registration.models import RegisteredSubject
from bhp_consent.managers import BaseConsentHistoryManager


class BaseConsentHistory(BaseUuidModel):

    """A base class for the consent history.

    Ties in with the consent model method :func:get_consent_history_model`, the manager method above
    and a signal in :mod:`bhp_consent.models.signals`

    .. note:: this is not a sync model so DO NOT turn off the signal when syncing. You want
              the history instances to be created by the incoming consent instances."""

    registered_subject = models.ForeignKey(RegisteredSubject)
    consent_datetime = models.DateTimeField()
    consent_pk = models.CharField(max_length=50)
    consent_app_label = models.CharField(max_length=50)
    consent_model_name = models.CharField(max_length=50)

    objects = BaseConsentHistoryManager()

    class Meta:
        abstract = True
