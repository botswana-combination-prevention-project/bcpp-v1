from datetime import datetime
from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_sync.models import Producer


class BaseDispatch(BaseUuidModel):
    """A base model for dispatching models to a mobile device
    """
    producer = models.ForeignKey(
        Producer,
        verbose_name="Producer / Netbook")

    is_dispatched = models.BooleanField(default=True)

    dispatch_datetime = models.DateTimeField(
        verbose_name="Dispatch date",
        default=datetime.today(),
        blank=True,
        null=True)

    return_datetime = models.DateTimeField(
        verbose_name="Return date",
        blank=True,
        null=True)

    class Meta:
        abstract = True
