from base_transaction import BaseTransaction


class Transaction(BaseTransaction):

    """ this model is not used """

    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']
