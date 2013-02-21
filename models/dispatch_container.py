from django.db import models
from base_dispatch import BaseDispatch


class DispatchContainer(BaseDispatch):

    container_app_label = models.CharField(max_length=35, null=True)
    container_model_name = models.CharField(max_length=35, null=True)
    container_identifier_attrname = models.CharField(max_length=35, null=True)
    container_identifier = models.CharField(max_length=35, null=True)
    container_pk = models.CharField(max_length=50, null=True)
    dispatched_using = models.CharField(max_length=35, null=True)
    dispatch_items = models.TextField(
        max_length=500,
        help_text='Dispatch items. One per line.')
    objects = models.Manager()

    def save(self, *args, **kwargs):
        # Before saving, make sure there aren't any items in the list that are dispatched
        # get a list of all dispatched items
        # TODO: does this have to be on the server?
#        DispatchItem = models.get_model('bhp_dispatch', 'DispatchItem')
#        items = [dispatch_item.item_identifier for dispatch_item in DispatchItem.objects.filter(dispatch__is_dispatched=True).exclude(dispatch__pk=self.pk)]
#        if self.__class__.objects.filter(dispatch_items__in=items, is_dispatched=True).exclude(pk=self.pk).exists():
#            dispatches = self.__class__.objects.filter(dispatch_items__in=items, is_dispatched=True).exclude(pk=self.pk)
#            raise ValueError("There are items in the list that are currently dispatched to {0}.".format([dispatch.producer.name for dispatch in dispatches]))
        super(DispatchContainer, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} @ {1}".format(self.producer.name, self.created)

    def to_items(self):
        DispatchItem = models.get_model('bhp_dispatch', 'DispatchItem')
        if DispatchItem.objects.filter(dispatch__pk=self.pk):
            return '<a href="/admin/bhp_dispatch/dispatchitem/?q={pk}">items</a>'.format(pk=self.pk)
        return None
    to_items.allow_tags = True

    class Meta:
        app_label = "bhp_dispatch"
