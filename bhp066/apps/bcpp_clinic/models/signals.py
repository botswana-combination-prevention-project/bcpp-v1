from django.db.models.signals import post_save
from django.dispatch import receiver

from .clinic_consent import ClinicConsent
from .clinic_eligibility import ClinicEligibility

# 
# @receiver(post_save, weak=False, dispatch_uid='subject_consent_on_post_save')
# def subject_consent_on_post_save(sender, instance, **kwargs):
#     if not kwargs.get('raw', False):
#         if isinstance(instance, ClinicConsent):
#             instance.post_save_update_registered_subject()


@receiver(post_save, weak=False, dispatch_uid="clinic_eligibility_on_post_save")
def clinic_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, ClinicEligibility):
            instance.update_registered_subject_on_post_save(**kwargs)
            if instance.is_eligible:
                instance.delete_enrollment_loss(**kwargs)
            else:
                instance.create_enrollment_loss(**kwargs)
