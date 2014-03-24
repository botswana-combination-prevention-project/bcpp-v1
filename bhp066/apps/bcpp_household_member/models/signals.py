from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver

from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel
from .household_member import HouseholdMember
from .subject_refusal import SubjectRefusal
from .subject_refusal_history import SubjectRefusalHistory
from .enrollment_checklist import EnrollmentChecklist


@receiver(pre_delete, weak=False, dispatch_uid="subject_refusal_on_pre_delete")
def subject_refusal_on_pre_delete(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, SubjectRefusal):
            # update the history model
            options = {'household_member': instance.household_member,
                       'survey': instance.survey,
                       'refusal_date': instance.refusal_date,
                       'reason': instance.reason,
                       'reason_other': instance.reason_other}
            SubjectRefusalHistory.objects.create(**options)


@receiver(post_delete, weak=False, dispatch_uid="subject_refusal_on_pre_delete")
def enrollment_checklist_on_pre_delete(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, EnrollmentChecklist):
            #re-save the member to recalc the member_status
            household_member = instance.household_member
            household_member.enrollment_checklist_completed = False
            household_member.eligible_subject = False
            household_member.save()


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_member_on_pre_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_member_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_registered_subject_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if isinstance(instance, BaseRegisteredHouseholdMemberModel):
        instance.confirm_registered_subject_pk_on_post_save()
