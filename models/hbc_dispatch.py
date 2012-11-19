from django.db import models
from bhp_checkout.classes import BaseCheckout


class HBCDispatch(BaseCheckout):

    checkout_items = models.TextField(
        max_length=500,
        help_text='Checked out households. One per line.'
        )

    def save(self, *args, **kwargs):
        # Before saving, make sure there isn't already an instance with the same cargo of household
        # identifiers that has checked out but not checked in yes
        if HBCDispatch.objects.filter(
                netbook=self.netbook,
                checkout_items=self.checkout_items,
                is_checked_out=True,
                is_checked_in=False,
                ).exclude(pk=self.pk).exists():
            raise ValueError("There are households already checked to {0} that have not been checked back in!".format(self.netbook))
        else:
            super(HBCDispatch, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} @ {1}".format(
                                self.netbook.name,
                                self.created
                                )

    class Meta:
        app_label = "mochudi_household"
