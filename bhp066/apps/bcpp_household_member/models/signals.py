from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel
from .enrollment_checklist import EnrollmentChecklist, EnrollmentLoss
from .household_member import HouseholdMember
from .subject_refusal import SubjectRefusal
from .subject_refusal_history import SubjectRefusalHistory


@receiver(post_delete, weak=False, dispatch_uid="subject_refusal_on_post_delete")
def subject_refusal_on_post_delete(sender, instance, using, **kwargs):
    if isinstance(instance, SubjectRefusal):
        # update the history model
        options = {'household_member': instance.household_member,
                   'survey': instance.survey,
                   'refusal_date': instance.refusal_date,
                   'reason': instance.reason,
                   'reason_other': instance.reason_other}
        SubjectRefusalHistory.objects.using(using).create(**options)
        household_member = instance.household_member
        household_member.refused = False
        household_member.save(using=using)


@receiver(post_delete, weak=False, dispatch_uid="enrollment_checklist_on_post_delete")
def enrollment_checklist_on_post_delete(sender, instance, using, **kwargs):
    if isinstance(instance, EnrollmentChecklist):
        # re-save the member to recalc the member_status
        # If this gets deleted, then the process must be started again from BHS_SCREEN
        household_member = instance.household_member
        try:
            EnrollmentLoss.objects.using(using).get(household_member=household_member).delete(using=using)
        except EnrollmentLoss.DoesNotExist:
            pass
        household_member.enrollment_checklist_completed = False
        household_member.enrollment_loss_completed = False
        household_member.eligible_subject = False
        household_member.save(using=using)


@receiver(post_save, weak=False, dispatch_uid="enrollment_checklist_on_post_save")
def enrollment_checklist_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, EnrollmentChecklist):
            instance.household_member.eligible_subject = False
            if instance.is_eligible:
                instance.household_member.eligible_subject = True
            instance.household_member.enrollment_checklist_completed = True
            instance.household_member.save(using=using)


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_member_on_pre_save(sender, instance, raw, using, **kwargs):
    if not raw:
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(using, **kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_member_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, HouseholdMember):
            instance.update_registered_subject_on_post_save(using, **kwargs)


@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, BaseRegisteredHouseholdMemberModel):
            instance.confirm_registered_subject_pk_on_post_save(using)
