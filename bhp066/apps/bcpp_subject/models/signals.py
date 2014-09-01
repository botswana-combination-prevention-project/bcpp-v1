from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bcpp_household_member.models import HouseholdMember

from .subject_consent import SubjectConsent

from ..classes import SubjectReferralHelper

from ..models import SubjectReferral

from apps.bcpp_household.models import HouseholdStructure


@receiver(post_save, weak=False, dispatch_uid='subject_consent_on_post_save')
def subject_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates household_structure and household_members to reflect enrollment and
    changed member status.

    Also, update_fields is set when verifying consents using the Admin action
    under edc.subject.consent. The list of fields is passed and trapped
    here to prevent further modifications to  household_structure and
    household_members.

    See also edc.subject.consent.actions.flag_as_verified_against_paper."""
    if not raw:
        if isinstance(instance, (SubjectConsent, )):
            if kwargs.get('updated_fields') != ['is_verified', 'is_verified_datetime']:
                instance.post_save_update_registered_subject(using)
                instance.household_member.is_consented = True
                instance.household_member.save(using=using, update_fields=['is_consented'])
                instance.household_member.household_structure.enrolled = True
                instance.household_member.household_structure.enrolled_household_member = instance.pk
                instance.household_member.household_structure.enrolled_datetime = instance.consent_datetime
                instance.household_member.household_structure.save(using=using,
                                                                   update_fields=['enrolled',
                                                                                  'enrolled_household_member',
                                                                                  'enrolled_datetime'])


@receiver(post_save, weak=False, dispatch_uid='update_subject_referral_on_post_save')
def update_subject_referral_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the subject referral if a model that is part of the referral data is changed."""
    if not raw:
        try:
            subject_visit = instance.visit
            subject_referral = SubjectReferral.objects.using(using).get(subject_visit=subject_visit)
            if instance.__class__ in SubjectReferralHelper(instance).models.values():
                subject_referral.save(using=using)
        except AttributeError:
            pass
        except SubjectReferral.DoesNotExist:
            pass
