from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from household_member import HouseholdStructure

@receiver(post_save, weak=False, dispatch_uid="household_structure_on_post_save")
def household_structure_on_post_save(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        if isinstance(instance, HouseholdStructure):
            instance.fetch_and_count_members_on_post_save(**kwargs)