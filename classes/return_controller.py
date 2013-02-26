from datetime import datetime
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.exceptions import DispatchContainerError, AlreadyReturned
from bhp_dispatch.models import DispatchContainer, DispatchItem
from base import Base


class ReturnController(Base):

    def get_dispatch_container_instances_for_producer(self, using=None):
        """Returns a queryset of DoispatchContainer instances for this producer that are disptched."""
        if not using:
            using = 'default'
        return DispatchContainer.objects.filter(producer=self.get_producer(), is_dispatched=True, return_datetime__isnull=True)

    def get_dispatched_item_instances_for_container(self, dispatch_container, using=None):
        """Returns a queryset of dispatched DispatchItem instances for this dispatch_container."""
        if not using:
            using = 'default'
        return DispatchItem.objects.filter(dispatch_container=dispatch_container, is_dispatched=True, return_datetime__isnull=True)

    def return_dispatched_items_for_container(self, dispatch_container, using=None):
        """Updates a queryset of dispatched DispatchItems to "no longer dispatched" for this dispatch_container."""
        #TODO: yes, this is inefficient. But can we check for just those items within this container efficiently?
        if not using:
            using = 'default'
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. '
                                          'Run bhp_sync first.'.format(self.get_producer_name()))
        if self.has_incoming_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on '
                                          'this server. Consume them first.'.format(self.get_producer_name()))
        DispatchItem.objects.using(using).filter(dispatch_container=dispatch_container, is_dispatched=True, return_datetime__isnull=True).update(
            return_datetime=datetime.now(),
            is_dispatched=False)

    def return_dispatched_container(self, dispatch_container):
        """Returns the dispatch container after first checking transactions and dispatch items."""
        if not dispatch_container:
            raise DispatchContainerError('Attribute dispatch_container may not be None.')
        # confirm dispatch container has not already been returned
        if not dispatch_container.is_dispatched and not dispatch_container.return_datetime:
            raise AlreadyReturned('The dispatch container {0} is not dispatched.'.format(dispatch_container))
        # confirm no pending transaction on the producer
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions. '
                                          'Run bhp_sync first.'.format(self.get_producer_name()))
        # confirm no pending transaction for this producer on the source
        if self.has_incoming_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending incoming transactions on '
                                          'this server. Consume them first.'.format(self.get_producer_name()))
        # confirm all dispatch items in the container are returned
        # TODO: does the dispatch container as a dispatch item cause a problem?
        if self.get_dispatched_item_instances_for_container(dispatch_container):
            raise DispatchContainerError('Dispatch container {0} has items that are still dispatched.'.format(dispatch_container))
        # return dispatch container
        dispatch_container.is_dispatched = False
        dispatch_container.return_datetime = datetime.today()
        dispatch_container.save()
        return True

    def return_dispatched_items(self):

        msgs = []
        for dispatch_container in self.get_dispatch_container_instances_for_producer():
            self.return_dispatched_items_for_container(dispatch_container)
#                msgs.append('Returned {0} items of {1} with {2}={3}'.format(dispatched_models.count(),
#                                                                            container.container_model_name,
#                                                                            container.container_identifier_attrname,
#                                                                            container.container_identifier))
#            else:
#                msgs.append('Nothing to return. There are no current dipatched items.')
        return msgs
