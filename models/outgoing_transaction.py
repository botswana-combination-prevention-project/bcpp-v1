from django.db import models
from base_transaction import BaseTransaction


class OutgoingTransaction(BaseTransaction):

    """ transactions produced locally to be consumed/sent to a queue or consumer """

    objects = models.Manager()

    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']
