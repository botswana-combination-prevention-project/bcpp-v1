from django.db import models
from django.core.exceptions import ValidationError
from base_dispatch import BaseDispatch
from dispatch_container import DispatchContainer


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
        using = kwargs.get('using', None)
        if self.__class__.objects.using(using).filter(
                item_identifier=self.item_identifier,
                is_dispatched=True,
                ).exclude(pk=self.pk).exists():
            dispatch_item = self.__class__.objects.using(using).get(
                item_identifier=self.item_identifier,
                is_dispatched=True,
                ).exclude(pk=self.pk)
            raise ValueError("Cannot dispatch. The item \'{0}\' is already dispatched to \'{1}\'.".format(dispatch_item.item_identifier, dispatch_item.dispatch_container.producer))
        if not self.dispatch_container:
            raise ValidationError('Attribute dispatch_container may not be None.')
        if self.is_dispatched and self.return_datetime:
            raise ValidationError('Attribute return_datetime must be None if is_dispatched=True.')
        if not self.is_dispatched and not self.return_datetime:
            raise ValidationError('Attribute \'return_datetime\' may not be None if \'is_dispatched\'=False.')

        super(DispatchItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Dispatch Item {0} {1} -> {2} ({3})".format(self.item_model_name, self.item_identifier, self.producer.name, self.is_dispatched)

    class Meta:
        app_label = "bhp_dispatch"
        unique_together = (('dispatch_container', 'item_pk', 'item_identifier', 'is_dispatched'), )
