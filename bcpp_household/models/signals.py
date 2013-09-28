from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from household import Plot, Household
from household_structure import HouseholdStructure


@receiver(pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")
def check_for_survey_on_pre_save(sender, instance, **kwargs):
    if isinstance(instance, (Plot, Household)):
        instance.check_for_survey_on_pre_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="create_household_structure_on_post_save")
def create_household_structure_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, Household):
            instance.create_household_structure_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="household_structure_on_post_save")
def household_structure_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdStructure):
            instance.create_household_log_on_post_save(**kwargs)
            instance.fetch_and_count_members_on_post_save(**kwargs)


@receiver(post_save, weak=False, dispatch_uid="create_household_on_post_save")
def create_household_on_post_save(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, Plot):
            instance.post_save_create_household(created)
