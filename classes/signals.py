from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, weak=False, dispatch_uid='is_checked_out_on_save')
def is_checked_out_on_save(sender, instance, **kwargs):
    """ Raise an exception if instance has been dipatched to a netbook
    but has not been checked back in.
    """
    #if isinstance(instance, BaseSyncModel):
    if 'subject_visit' in dir(instance):
        if instance.subject_visit.is_locked():
            message = "{0} is currently dispatched to a netbook NOT synced with the server".format(instance.subject_visit.household_structure_member)
            raise ValueError(message)

    elif 'household_structure_member' in dir(instance):
        if instance.household_structure_member.is_locked():
            message = "{0} is currently dispatched to a netbook NOT synced with the server".format(instance.household_structure_member)
            raise ValueError(message)
