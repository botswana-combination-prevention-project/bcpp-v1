from django.dispatch import receiver
from django.db.models.signals import post_save
try:
    from bhp_sync.classes import BaseSyncModel
except ImportError:
    pass
from bhp_base_model.classes import BaseUuidModel
from bhp_bucket.classes import bucket

from rule_history import RuleHistory

@receiver(post_save, weak=False, dispatch_uid='model_bucket_rules_on_save' )
def model_bucket_rules_on_save(sender, instance, **kwargs):
    """ update / run model bucket rules, see bhp_bucket """
    if isinstance(instance, (BaseUuidModel, BaseSyncModel)):
        bucket.update(instance)