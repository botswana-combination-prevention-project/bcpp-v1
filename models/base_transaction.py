# requires django-extensions 0.7
from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicModel
from bhp_common.fields import MyUUIDField
from bhp_sync.managers import TransactionManager
from bhp_sync.classes import TransactionProducer

transaction_producer = TransactionProducer()

class BaseTransaction(MyBasicModel):
    
    id = MyUUIDField(primary_key=True)
    
    tx_name = models.CharField(
        max_length = 64,
        )
    
    tx_pk = models.CharField(
        max_length = 36,
        )
    
    tx = models.TextField()
    
    producer = models.CharField(
        max_length = 25,
        default = str(transaction_producer),
        db_index = True,
        )

    action = models.CharField(
        max_length = 1,
        default='I',
        choices = (('I', 'Insert'), ('U', 'Update'),('D', 'Delete')), 
        )
    
    timestamp = models.CharField(
        max_length = 50,    
        null = True,
        db_index = True,
        )
    
    is_consumed = models.BooleanField(
        default = False,
        )
    
    consumed_datetime = models.DateTimeField(
        null = True,
        blank = True,
        )

    consumer = models.CharField(
        max_length = 25,
        null = True,
        blank = True,
        db_index = True,
        )
    
    error = models.CharField(
         max_length = 1000,
         null = True,
         blank = True,
         )

    batch_seq = models.IntegerField(null=True, blank=True)
    
    batch_id = models.IntegerField(null=True, blank=True)

    objects = TransactionManager()

    def is_serialized(self):
        return False
        
    def save(self, *args, **kwargs):

        if self.is_consumed is True and not self.consumed_datetime:
            self.consumed_datetime = datetime.today()
        
        super(BaseTransaction, self).save(*args, **kwargs)

    
    class Meta:
        abstract = True

