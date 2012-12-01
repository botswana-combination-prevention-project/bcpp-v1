from django.db import models
from base_dispatch import BaseDispatch


class Dispatch(BaseDispatch):

    dispatch_items = models.TextField(
        max_length=500,
        help_text='Dispatch items. One per line.'
        )
    objects = models.Manager()

    def save(self, *args, **kwargs):
        # Before saving, make sure there isn't already an instance with the same cargo of household
        # identifiers that has checked out but not checked in yes
        if self.__class__.objects.filter(
                producer=self.producer,
                dispatch_items=self.dispatch_items,
                is_dispatched=True,
                ).exclude(pk=self.pk).exists():
            raise ValueError("There are items in the list that are currently dispatched to {0}.".format(self.producer))
        else:
            super(Dispatch, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} @ {1}".format(self.producer.name, self.created)

    class Meta:
        app_label = "bhp_dispatch"
