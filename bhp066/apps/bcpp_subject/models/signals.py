from django.db.models.signals import post_save
from django.dispatch import receiver

from .subject_consent import SubjectConsent


@receiver(post_save, weak=False, dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, (SubjectConsent)):
            instance.post_save_update_registered_subject()  # HM values must either be changed or match that provided on the consent
            instance.household_member.enroll_household()
