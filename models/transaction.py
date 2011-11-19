# requires django-extensions 0.7
# from django_extensions.db.fields import json as jsonfield
import socket
import settings
from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_sync.managers import TransactionManager


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
        default = '%s-%s' % ( socket.gethostname().lower(),settings.DATABASES['default']['NAME'].lower()),
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
    
    is_sent = models.BooleanField(
        default = False
        )
    
    sent_datetime = models.DateTimeField(
        null = True,
        )

    objects = TransactionManager()
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp'] 
