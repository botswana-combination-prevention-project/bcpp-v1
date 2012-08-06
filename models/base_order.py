from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.validators import datetime_not_future
from lab_panel.models import Panel


class BaseOrder(BaseUuidModel):

    order_identifier = models.CharField(
        verbose_name='Order number',
        max_length=25,
        help_text='Allocated internally',
        db_index=True,
        editable=False,
        )

    order_datetime = models.DateTimeField(
        verbose_name='Order Date',
        validators=[datetime_not_future],
        db_index=True,
        )

    panel = models.ForeignKey(Panel)

    comment = models.CharField(
        verbose_name='Comment',
        max_length=150,
        null=True,
        blank=True,
        )

    dmis_reference = models.IntegerField(
        null=True,
        blank=True,
        )

    def __unicode__(self):
        return '%s %s' % (self.order_identifier, self.panel)

    class Meta:
        abstract = True
