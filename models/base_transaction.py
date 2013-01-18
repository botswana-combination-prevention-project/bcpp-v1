# requires django-extensions 0.7
from datetime import datetime
from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_sync.classes import TransactionProducer


transaction_producer = TransactionProducer()


class BaseTransaction(BaseUuidModel):

    tx = models.TextField()

    tx_name = models.CharField(
        max_length=64,
        db_index=True,
        )

    tx_pk = models.CharField(
        max_length=36,
        )

    producer = models.CharField(
        max_length=25,
        default=str(transaction_producer),
        db_index=True,
        )

    action = models.CharField(
        max_length=1,
        default='I',
        choices=(('I', 'Insert'), ('U', 'Update'), ('D', 'Delete')),
        )

    timestamp = models.CharField(
        max_length=50,
        null=True,
        db_index=True,
        )

    is_consumed = models.BooleanField(
        default=False,
        db_index=True,
        )

    consumed_datetime = models.DateTimeField(
        null=True,
        blank=True,
        )

    consumer = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        db_index=True,
        )

    is_ignored = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Ignore if update'
        )

    is_error = models.BooleanField(
        default=False,
        db_index=True,
        )

    error = models.TextField(
         max_length=1000,
         null=True,
         blank=True,
         )

    batch_seq = models.IntegerField(null=True, blank=True)

    batch_id = models.IntegerField(null=True, blank=True)

    def is_serialized(self):
        return False

    def save(self, *args, **kwargs):

        if self.is_consumed is True and not self.consumed_datetime:
            self.consumed_datetime = datetime.today()
        super(BaseTransaction, self).save(*args, **kwargs)

    class Meta:
        abstract = True
