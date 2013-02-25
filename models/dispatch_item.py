from django.db import models
from base_dispatch import BaseDispatch
from dispatch_container import DispatchContainer
from bhp_sync.classes import Consumer


class DispatchItem(BaseDispatch):
    dispatch_container = models.ForeignKey(DispatchContainer)
    item_app_label = models.CharField(max_length=35, null=True)
    item_model_name = models.CharField(max_length=35, null=True)
    item_identifier_attrname = models.CharField(max_length=35, null=True)
    item_identifier = models.CharField(max_length=35, null=True)
    item_pk = models.CharField(max_length=50, null=True)
    dispatch_host = models.CharField(max_length=35, null=True)
    dispatch_using = models.CharField(max_length=35, null=True)
    registered_subjects = models.TextField(
        verbose_name='List of Registered Subjects',
        null=True,
        blank=True,
        help_text="List of Registered Subjects linked to this DispatchItem"
        )
    objects = models.Manager()



# temp removed - erikvw (fails on unknown producer when setting dispatched to False)
# no longer necessary to check if the instance is dispatched, as this is done by
# the controller class.
    def save(self, *args, **kwargs):
        """Confirms an instance does not exist for this item_identifier."""
        if self.__class__.objects.filter(
                item_identifier=self.item_identifier,
                is_dispatched=True,
                ).exclude(pk=self.pk).exists():
            dispatch_item = self.__class__.objects.get(
                item_identifier=self.item_identifier,
                is_dispatched=True,
                ).exclude(pk=self.pk)
            raise ValueError("Cannot dispatch. The item \'{0}\' is already dispatched to \'{1}\'.".format(dispatch_item.item_identifier, dispatch_item.dispatch_container.producer))
#        if not self.is_dispatched:
#            self.run_pre_unlocking_checks()
        super(DispatchItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} -> {1}".format(self.item_identifier, self.producer.name)

    class Meta:
        app_label = "bhp_dispatch"
        unique_together = (('item_identifier', 'is_dispatched'), )
