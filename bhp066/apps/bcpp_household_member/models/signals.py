from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from ..classes import HouseholdMemberHelper

from .base_registered_household_member_model import BaseRegisteredHouseholdMemberModel
from .household_member import HouseholdMember
from .subject_refusal import SubjectRefusal
from .subject_refusal_history import SubjectRefusalHistory


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


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_member_on_pre_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_member_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_registered_subject_on_post_save(**kwargs)  # update HM must not override consent values, if consent exists
            instance.update_household_member_count_on_post_save(sender, using)
            if created:
                # calculate member status
                household_member_helper = HouseholdMemberHelper()
                household_member_helper.household_member = instance
                instance.member_status = household_member_helper.calculate_new_member_status()
                instance.save()
                # has members so confirm household enumerated is True
                if not instance.household_structure.household.enumerated:
                    instance.household_structure.household.enumerated = True
                    instance.household_structure.household.save()



@receiver(post_save, weak=False, dispatch_uid='base_household_member_consent_on_post_save')
def base_household_member_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if isinstance(instance, BaseRegisteredHouseholdMemberModel):
        instance.confirm_registered_subject_pk_on_post_save()
