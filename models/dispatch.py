from django.db import models
from base_dispatch import BaseDispatch


class Dispatch(BaseDispatch):

    dispatch_items = models.TextField(
        max_length=500,
        help_text='Dispatch items. One per line.'
        )
    objects = models.Manager()

    def save(self, *args, **kwargs):
        # Before saving, make sure there aren't any items in the list that are dispatched
        # get a list of all dispatched items
        # TODO: does this have to be on the server?
        DispatchItem = models.get_model('bhp_dispatch', 'DispatchItem')
        items = [dispatch_item.item_identifier for dispatch_item in DispatchItem.objects.filter(dispatch__is_dispatched=True).exclude(dispatch__pk=self.pk)]
        if self.__class__.objects.filter(dispatch_items__in=items, is_dispatched=True).exclude(pk=self.pk).exists():
            dispatches = self.__class__.objects.filter(dispatch_items__in=items, is_dispatched=True).exclude(pk=self.pk)
            raise ValueError("There are items in the list that are currently dispatched to {0}.".format([dispatch.producer.name for dispatch in dispatches]))
        super(Dispatch, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} @ {1}".format(self.producer.name, self.created)

    class Meta:
        app_label = "bhp_dispatch"
