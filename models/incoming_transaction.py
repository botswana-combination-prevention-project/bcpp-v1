import socket
from django.db import models
from datetime import datetime
from base_transaction import BaseTransaction
from bhp_sync.managers import IncomingTransactionManager


class IncomingTransaction(BaseTransaction):

    """ Transactions received from a remote producer and to be consumed locally. """
    is_consumed = models.BooleanField(
        default=False,
        db_index=True,
        )
    is_self = models.BooleanField(
        default=False,
        db_index=True)
    objects = IncomingTransactionManager()

    def save(self, *args, **kwargs):
        """ An incoming transaction produced by self may exist, but is not wanted, if received by fanout from a consumer of
        transactions of self (this producer). that is (hostname_modified==hostname)."""
        #TODO: for IncomingTransaction perhaps just cancel save instead??
        if self.hostname_modified == socket.gethostname():
            #self.is_consumed = True
            self.is_self = True
        if self.is_consumed and not self.consumed_datetime:
            self.consumed_datetime = datetime.today()
        super(IncomingTransaction, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']
