from django.db.models.signals import post_delete
from django.dispatch import receiver
from bhp_base_model.models import BaseModel
from excluded import Excluded


@receiver(post_delete, weak=False, dispatch_uid='supplemental_fields_on_post_delete')
def supplemental_fields_on_post_delete(sender, instance, **kwargs):
    if isinstance(instance, (BaseModel)):
        Excluded.objects.filter(model_pk=instance.pk).delete()
