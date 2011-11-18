# requires django-extensions 0.7
from django_extensions.db.fields import json as jsonfield
from django.db import models
from bhp_common.models import MyBasicUuidModel



class Transaction(MyBasicUuidModel):
    
    tx_name = models.CharField(
        max_length = 64,
        )
    
    tx_pk = models.CharField(
        max_length = 36,
        )
    
    tx = jsonfield.JSONField()
    
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
    
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['timestamp'] 
