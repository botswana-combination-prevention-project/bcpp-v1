from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.validators import datetime_not_future
from lab_order.choices import ORDER_STATUS


class BaseOrder(BaseUuidModel):

    order_identifier = models.CharField(
        verbose_name='Order number',
        max_length=25,
        help_text='Allocated internally',
        db_index=True,
        editable=False)
    order_datetime = models.DateTimeField(
        verbose_name='Order Date',
        validators=[datetime_not_future],
        db_index=True)
    status = models.CharField(
        verbose_name='Status',
        max_length=25,
        choices=ORDER_STATUS,
        null=True,
        blank=False)
    comment = models.CharField(
        verbose_name='Comment',
        max_length=150,
        null=True,
        blank=True)
    receive_identifier = models.CharField(
        max_length=25, editable=False, null=True, db_index=True,
        help_text="non-user helper field to simplify search and filter")
    import_datetime = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.receive_identifier = self.order.aliquot.receive_identifier
        super(BaseOrder, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s' % (self.order_identifier, self.panel)

    class Meta:
        abstract = True
