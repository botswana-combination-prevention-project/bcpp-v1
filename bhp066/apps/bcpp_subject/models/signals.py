from django.db.models.signals import post_save
from django.dispatch import receiver
from .base_household_member_consent import BaseHouseholdMemberConsent


@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save2')
def base_household_member_consent_on_post_save2(sender, instance, **kwargs):
    if isinstance(instance, (BaseHouseholdMemberConsent)):
        instance.post_save_update_registered_subject()  # HM values must either be changed or match that provided on the consent
