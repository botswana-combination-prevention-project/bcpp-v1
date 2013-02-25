from datetime import datetime
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.models import DispatchContainer, DispatchItem
from base import Base


class ReturnController(Base):

    def get_dispatch_container_instances_for_producer(self):
        return DispatchContainer.objects.filter(producer=self.get_producer(), is_dispatched=True)

    def get_dispatch_item_instances_for_container(self, dispatch_container):
        return DispatchItem.objects.filter(dispatch_container=dispatch_container)

    def return_dispatch_items_for_container(self, dispatch_container):
        DispatchItem.objects.filter(dispatch_container=dispatch_container).update(
            return_datetime=datetime.now(),
            is_dispatched=False)

    def return_dispatched_items(self):
        msgs = []
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. '
                                          'Run bhp_sync first.'.format(self.get_producer_name()))
        if self.has_incoming_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on '
                                          'this server. Consume them first.'.format(self.get_producer_name()))
        else:
            for dispatch_container in self.get_dispatch_container_instances_for_producer():
                self.return_dispatch_items_for_container(dispatch_container)
#                msgs.append('Returned {0} items of {1} with {2}={3}'.format(dispatched_models.count(),
#                                                                            container.container_model_name,
#                                                                            container.container_identifier_attrname,
#                                                                            container.container_identifier))
#            else:
#                msgs.append('Nothing to return. There are no current dipatched items.')
        return msgs
