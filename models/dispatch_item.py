from django.db import models
from base_dispatch import BaseDispatch
from dispatch import Dispatch


class DispatchItem(BaseDispatch):

    dispatch = models.ForeignKey(Dispatch)
    item_identifier = models.CharField(
        verbose_name='Item Identifier',
        max_length=25,
        help_text="Dispatch Item (e.g. Household Identifier)"
        )
    subject_identifiers = models.TextField(
        verbose_name='Subject Identifiers',
        null=True,
        blank=True,
        help_text="Subject identifiers associated with this Dispatch Item"
        )
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.__class__.objects.filter(
                producer=self.producer,
                item_identifier=self.item_identifier,
                is_dispatched=True,
                ).exclude(pk=self.pk).exists():
            raise ValueError("The item {0} is currently dispatched to {1}.".format(self.item_identifier, self.producer))
        else:
            super(DispatchItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} -> {1}".format(self.item_identifier, self.producer.name)

    class Meta:
        app_label = "bhp_dispatch"
