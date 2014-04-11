from django.db.models.signals import post_save
from django.dispatch import receiver

from .subject_consent import SubjectConsent

from ..classes import SubjectReferralHelper

from ..models import SubjectReferral


@receiver(post_save, weak=False, dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, (SubjectConsent)):
            instance.post_save_update_registered_subject()  # HM values must either be changed or match that provided on the consent
            instance.household_member.enroll_household()


@receiver(post_save, weak=False, dispatch_uid='update_subject_referral_on_post_save')
def update_subject_referral_on_post_save(sender, instance, **kwargs):
    """Updates the subject referral if a model that is part of the referral data is changed."""
    if not kwargs.get('raw', False):
        try:
            subject_visit = instance.visit
            subject_referral = SubjectReferral.objects.get(subject_visit=subject_visit)
            if instance.__class__ in SubjectReferralHelper(instance).models.values():
                subject_referral.save()
        except AttributeError:
            pass
        except SubjectReferral.DoesNotExist:
            pass
