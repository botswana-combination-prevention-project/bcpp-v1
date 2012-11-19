from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_sync.models import Producer


class BaseDispatch(BaseUuidModel):
    """A base model for checking out/in models to a mobile device
    """
    producer = models.ForeignKey(
        Producer,
        verbose_name="Producer / Netbook"
        )

    is_checked_out = models.BooleanField(
        default=False
        )

    is_checked_in = models.BooleanField(
        default=False
        )

    datetime_checked_out = models.DateTimeField(
        verbose_name="Check-out date",
        blank=True,
        null=True
        )

    datetime_checked_in = models.DateTimeField(
        verbose_name="Check-in date",
        blank=True,
        null=True
        )

    class Meta:
        abstract = True
