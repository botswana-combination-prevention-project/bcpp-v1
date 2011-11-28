# requires django-extensions 0.7
# from django_extensions.db.fields import json as jsonfield
from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_sync.managers import TransactionManager
from bhp_sync.classes import TransactionProducer

transaction_producer = TransactionProducer()

class Transaction(MyBasicUuidModel):
    
    tx_name = models.CharField(
        max_length = 64,
        )
    
    tx_pk = models.CharField(
        max_length = 36,
        )
    
    # tx = jsonfield.JSONField()
    
    tx = models.TextField()
    
    producer = models.CharField(
        max_length = 15,
        default = str(transaction_producer),
        )

    action = models.CharField(
        max_length = 1,
        default='I',
        choices = (('I', 'Insert'), ('U', 'Update'),('D', 'Delete')), 
        )
    
    timestamp = models.CharField(
        max_length = 50,    
        null = True,
        )
    
    is_consumed = models.BooleanField(
        default = False
        )
    
    consumed_datetime = models.DateTimeField(
        null = True,
        blank = True,
        )

    consumer = models.CharField(
        max_length = 15,
        null = True,
        blank = True,
        )

    objects = TransactionManager()

    def is_serialized(self):
        return False
        
    def save(self, *args, **kwargs):
        
        if self.is_consumed is True and not self.consumed_datetime:
            self.consumed_datetime = datetime.today()
        super(Transaction, self).save(*args, **kwargs)
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp'] 
