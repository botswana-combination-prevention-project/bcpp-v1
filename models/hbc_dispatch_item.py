from django.db import models
from bhp_checkout.classes import BaseCheckout
from mochudi_household.models import HBCDispatch


class HBCDispatchItem(BaseCheckout):

    hbc_dispatch = models.ForeignKey(HBCDispatch, null=True)
    household_identifier = models.CharField(
        verbose_name='Household Identifier',
        max_length=25,
        help_text="Checked out Household identifier"
        )
    objects = models.Manager()

    def save(self, *args, **kwargs):
        if HBCDispatchItem.objects.filter(
                netbook=self.netbook,
                household_identifier=self.household_identifier,
                is_checked_out=True,
                is_checked_in=False,
                ).exclude(pk=self.pk).exists():
            raise ValueError("The household {0} has already been checked to {1} but have not been checked back in!".format(self.household_identifier, self.netbook))
        else:
            super(HBCDispatchItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} -> {1}".format(
                                self.household_identifier,
                                self.netbook.name
                                )

    class Meta:
        app_label = "bhp_dispatch"
