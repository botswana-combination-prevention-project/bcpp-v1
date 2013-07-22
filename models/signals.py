from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from household_member import HouseholdMember, HouseholdStructure


@receiver(pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
def household_structure_member_on_pre_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_hiv_history_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_member_on_post_save")
def household_structure_member_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdMember):
            instance.update_registered_subject_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_structure_on_post_save")
def household_structure_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdStructure):
            instance.fetch_and_count_members_on_post_save(**kwargs)