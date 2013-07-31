from django.db import models
from base_transaction import BaseTransaction


class MiddleManTransaction(BaseTransaction):

    """ transactions produced locally to be consumed/sent to a queue or consumer """

    is_consumed_middleman = models.BooleanField(
        default=False,
        db_index=True,
        )
    
    is_consumed_server = models.BooleanField(
        default=False,
        db_index=True,
        )
    
    objects = models.Manager() 
    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']