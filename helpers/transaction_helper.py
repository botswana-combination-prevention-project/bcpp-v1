from bhp_sync.models import OutgoingTransaction, IncomingTransaction


class TransactionHelper(object):

    def has_incoming_for_producer(self, producer, using=None):
        if not using:
            using = 'default'
        return IncomingTransaction.objects.using(using).filter(producer=producer, is_consumed=False).exists()

    def has_incoming_for_model(self, models, using=None):
        if not models:
            return False
        if not using:
            using = 'default'
        if not isinstance(models, (list, tuple)):
            models = [models]
        return IncomingTransaction.objects.using(using).filter(tx_name__in=models, is_consumed=False).exists()

    def has_outgoing(self, using=None):
        return OutgoingTransaction.objects.using(using).filter(is_consumed=False).exists()
