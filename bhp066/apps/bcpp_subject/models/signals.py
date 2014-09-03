from django.db.models.signals import post_save
from django.dispatch import receiver

from edc.core.bhp_data_manager.models import TimePointStatus
from edc.constants import CLOSED

from .subject_consent import SubjectConsent

from ..classes import SubjectReferralHelper

from ..models import SubjectReferral, SubjectVisit


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
                # update household_structure if enrolled
                instance.household_member.household_structure.enrolled = True
                instance.household_member.household_structure.enrolled_household_member = instance.pk
                instance.household_member.household_structure.enrolled_datetime = instance.consent_datetime
                instance.household_member.household_structure.save(using=using,
                                                                   update_fields=['enrolled',
                                                                                  'enrolled_household_member',
                                                                                  'enrolled_datetime'])
                # update household if enrolled
                instance.household_member.household_structure.household.enrolled = True
                instance.household_member.household_structure.household.enrolled_datetime = \
                    instance.consent_datetime
                instance.household_member.household_structure.household.save(
                    using=using, update_fields=['enrolled', 'enrolled_datetime'])
                # update plot if enrolled
                instance.household_member.household_structure.household.plot.bhs = True
                instance.household_member.household_structure.household.plot.enrolled_datetime = \
                    instance.consent_datetime
                instance.household_member.household_structure.household.plot.save(
                    using=using, update_fields=['bhs', 'enrolled_datetime'])


@receiver(post_save, weak=False, dispatch_uid='update_subject_referral_on_post_save')
def update_subject_referral_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the subject referral if a model that is part of the referral data is changed.

    The sender classes are listed in the SubjectReferralHelper."""
    if not raw:
        try:
            if sender in SubjectReferralHelper.models.values():
                subject_referral = SubjectReferral.objects.using(using).get(subject_visit=instance.visit)
                subject_referral.save(using=using)
        except AttributeError:
            pass
        except SubjectReferral.DoesNotExist:
            pass


@receiver(post_save, weak=False, dispatch_uid='time_point_status_on_post_save')
def time_point_status_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Attempt to save the subject referral to refer participants that
    do not complete data collection (partial participation)."""
    if not raw:
        if isinstance(instance, (TimePointStatus, )):
            if instance.status == CLOSED:
                try:
                    subject_visit = SubjectVisit.objects.get(appointment=instance.appointment)
                    SubjectReferral.objects.using(using).get(
                        subject_visit=subject_visit)
                except SubjectReferral.DoesNotExist:
                    # create a new document and flag as partial
                    SubjectReferral.objects.using(using).create(
                        subject_visit=subject_visit,
                        subject_referred='No',
                        comment='(Partial participation. Auto generated when time point closed.)'
                        )
