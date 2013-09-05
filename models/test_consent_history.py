from django.db import models
from bhp_consent.models import BaseConsentHistory
from bhp_consent.managers import BaseConsentHistoryManager


class ConsentHistoryManager(BaseConsentHistoryManager):

    def update_consent_history(self, consent_inst, created, using):
        updated_values = {'consent_datetime': consent_inst.consent_datetime}
        inst, created = super(ConsentHistoryManager, self).using(using).get_or_create(
            registered_subject=consent_inst.registered_subject,
            consent_app_label=consent_inst._meta.app_label,
            consent_model_name=consent_inst._meta.object_name,
            consent_pk=consent_inst.pk,
            defaults=updated_values
            )
        if not created:
            inst.consent_datetime = consent_inst.consent_datetime
            inst.save(using=using)


class TestConsentHistory(BaseConsentHistory):

    objects = ConsentHistoryManager()

    class Meta:
        app_label = 'bhp_base_test'
