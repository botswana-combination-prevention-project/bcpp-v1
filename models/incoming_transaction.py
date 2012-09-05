import socket
from django.db import models
from django.core.urlresolvers import reverse
from base_transaction import BaseTransaction
from bhp_sync.managers import IncomingTransactionManager
#from bhp_crypto.fields import EncryptedTextField


class IncomingTransaction(BaseTransaction):

    """ Transactions received from a remote producer and to be consumed locally. """

    is_self = models.BooleanField(
        default=False,
        db_index=True)
    objects = IncomingTransactionManager()

    def render(self):
        url = reverse('view_transaction_url', kwargs={'model_name': self._meta.object_name.lower(), 'pk': self.pk})
        ret = """<a href="{url}" class="add-another" id="add_id_report" onclick="return showAddAnotherPopup(this);"> <img src="/static/admin/img/icon_addlink.gif" width="10" height="10" alt="View transaction"/></a>""".format(url=url)
        return ret
    render.allow_tags = True

    def save(self, *args, **kwargs):
        """ An incoming transaction produced by self may exist, but is not wanted, if received by fanout from a consumer of
        transactions of self (this producer). that is (hostname_modified==hostname)."""
        #TODO: for IncomingTransaction perhaps just cancel save instead??
        if self.hostname_modified == socket.gethostname():
            #self.is_consumed = True
            self.is_self = True
        super(IncomingTransaction, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']
