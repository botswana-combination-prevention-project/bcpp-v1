from bhp_consent.managers import BaseConsentHistoryManager


class ConsentHistoryManager(BaseConsentHistoryManager):

    def update_consent_history(self, consent_inst, created, using):
        updated_values = {'consent_datetime': consent_inst.consent_datetime,
                          'survey': consent_inst.survey,
                          'household_member': consent_inst.household_member}
        inst, created = super(ConsentHistoryManager, self).using(using).get_or_create(
            registered_subject=consent_inst.registered_subject,
            consent_app_label=consent_inst._meta.app_label,
            consent_model_name=consent_inst._meta.object_name,
            consent_pk=consent_inst.pk,
            defaults=updated_values
            )
        if not created:
            inst.consent_datetime = consent_inst.consent_datetime
            inst.consent_datetime = consent_inst.survey
            inst.consent_datetime = consent_inst.household_member
            inst.save(using=using)
