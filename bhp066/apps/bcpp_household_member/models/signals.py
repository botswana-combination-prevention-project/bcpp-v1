from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .household_member import HouseholdMember
from .base_member_status_model import BaseMemberStatusModel
from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_member_on_pre_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_member_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_registered_subject_on_post_save(**kwargs)  # update HM must not override consent values, if consent exists
            instance.update_household_member_count_on_post_save(**kwargs)
            if instance.member_status == 'ABSENT':
                # TODO: probably do not need to call this now??
                instance.subject_absentee


@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, **kwargs):
    if isinstance(instance, (BaseMemberStatusModel)):
        instance.post_save_update_hm_status()  # HM values must either be changed or match that provided on the consent
    if isinstance(instance, BaseRegisteredHouseholdMemberModel):
        instance.confirm_registered_subject_pk_on_post_save()
