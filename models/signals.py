from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, weak=False, dispatch_uid='is_dispatched_on_save')
def is_dispatched_on_save(sender, instance, **kwargs):
    """ Raise an exception if instance is dispatched to a device."""
    if 'is_dispatched' in dir(instance):
        if instance.is_dispatched():
            message = "{0} is currently dispatched to a device. Cannot save. Refer to models Dispatch/DispatchItems".format(instance)
            raise ValueError(message)
