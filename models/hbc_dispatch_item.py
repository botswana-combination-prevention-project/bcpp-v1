from django.db import models
from bhp_dispatch.classes import BaseDispatch
from hbc_dispatch import HBCDispatch


class HBCDispatchItem(BaseDispatch):

    hbc_dispatch = models.ForeignKey(HBCDispatch, null=True)
    item_identifier = models.CharField(
        verbose_name='Item Identifier',
        max_length=25,
        help_text="Checked out Item (e.g. Household Identifier)"
        )
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.objects.filter(
                producer=self.producer,
                item_identifier=self.item_identifier,
                is_checked_out=True,
                is_checked_in=False,
                ).exclude(pk=self.pk).exists():
            raise ValueError("The item {0} has already been checked to {1} but have not been checked back in!".format(self.item_identifier, self.producer))
        else:
            super(HBCDispatchItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} -> {1}".format(
                                self.item_identifier,
                                self.producer.name
                                )

    class Meta:
        app_label = "bhp_dispatch"
