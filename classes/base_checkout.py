from datetime import datetime
from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_sync.models import Producer


class BaseCheckout(BaseUuidModel):
    """A base model for checking out/in models to a mobile device
    """
    netbook = models.ForeignKey(
        Producer,
        verbose_name="Netbook"
        )

    is_checked_out = models.BooleanField(
        default=False
        )

    is_checked_in = models.BooleanField(
        default=False
        )

    datetime_checked_out = models.DateTimeField(
        verbose_name="Checkout date",
        blank=True,
        null=True
        )

    datetime_checked_in = models.DateTimeField(
        verbose_name="Checkin date",
        blank=True,
        null=True
        )

    class Meta:
        abstract = True
