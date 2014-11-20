from datetime import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.bcpp_household_member.constants import NOT_ELIGIBLE, CLINIC_RBD

from .clinic_consent import ClinicConsent
from .clinic_eligibility import ClinicEligibility
from .clinic_enrollment_loss import ClinicEnrollmentLoss
from .clinic_household_member import ClinicHouseholdMember
from .clinic_refusal import ClinicRefusal
from .clinic_refusal_history import ClinicRefusalHistory


@receiver(post_save, weak=False, dispatch_uid="clinic_eligibility_on_post_save")
def clinic_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates the household_member instance, if it does not exist, and if not eligible,
    creates a ClinicEnrollmentLoss instance."""
    if not raw:
        if isinstance(instance, ClinicEligibility):
            clinic_household_member = ClinicHouseholdMember.objects.get(pk=instance.household_member.pk)
            clinic_household_member.registered_subject.identity = instance.identity
            clinic_household_member.registered_subject.identity_type = instance.identity_type
            clinic_household_member.registered_subject.save()
            if not instance.is_eligible:
                try:
                    clinic_enrollment_loss = ClinicEnrollmentLoss.objects.get(household_member=instance.household_member)
                    clinic_enrollment_loss.report_datetime = instance.report_datetime
                    clinic_enrollment_loss.reason = '; '.join(instance.loss_reason or [])
                    clinic_enrollment_loss.user_modified = instance.user_modified
                    clinic_enrollment_loss.save()
                except ClinicEnrollmentLoss.DoesNotExist:
                    ClinicEnrollmentLoss.objects.create(
                        household_member=clinic_household_member,
                        report_datetime=instance.report_datetime,
                        reason='; '.join(instance.loss_reason or []),
                        user_created=instance.user_created,
                        user_modified=instance.user_modified)
                clinic_household_member.member_status = NOT_ELIGIBLE
                clinic_household_member.enrollment_loss_completed = True
                clinic_household_member.save(update_fields=['member_status', 'enrollment_loss_completed'])
            else:
                ClinicEnrollmentLoss.objects.filter(household_member=instance.household_member).delete()
                clinic_household_member.member_status = CLINIC_RBD
                clinic_household_member.enrollment_loss_completed = False
                clinic_household_member.save(update_fields=['member_status', 'enrollment_loss_completed'])


@receiver(post_save, weak=False, dispatch_uid="clinic_consent_on_post_save")
def clinic_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the is_consented boolean on the eligibility checklist."""
    if not raw:
        if isinstance(instance, ClinicConsent):
            clinic_eligibility = ClinicEligibility.objects.get(household_member=instance.household_member)
            clinic_eligibility.is_consented = True
            clinic_eligibility.save(update_fields=['is_consented'])
            ClinicRefusal.objects.filter(household_member=instance.household_member).delete()


@receiver(post_save, weak=False, dispatch_uid="clinic_refusal_on_post_save")
def clinic_refusal_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Updates the is_refused boolean on the eligibility checklist."""
    if not raw:
        if isinstance(instance, ClinicRefusal):
            clinic_eligibility = ClinicEligibility.objects.get(household_member=instance.household_member)
            clinic_eligibility.is_refused = True
            clinic_eligibility.save(update_fields=['is_refused'])


@receiver(post_delete, weak=False, dispatch_uid="clinic_refusal_on_post_delete")
def clinic_refusal_on_post_delete(sender, instance, using, **kwargs):
    """Delete refusal but first puts a copy into the history model."""
    if isinstance(instance, ClinicRefusal):
        # update the history model
        options = {'household_member': instance.household_member,
                   'refusal_date': instance.refusal_date,
                   'report_datetime': datetime.today(),
                   'survey': instance.household_member.household_structure.survey,
                   'refusal_date': instance.refusal_date,
                   'reason': instance.reason,
                   'reason_other': instance.reason_other}
        ClinicRefusalHistory.objects.using(using).create(**options)
        clinic_eligibility = ClinicEligibility.objects.get(household_member=instance.household_member)
        clinic_eligibility.is_refused = False
        clinic_eligibility.save(update_fields=['is_refused'])