from datetime import datetime
from bhp_sync.exceptions import PendingTransactionError
from bhp_dispatch.exceptions import DispatchContainerError, AlreadyReturned
from bhp_dispatch.models import DispatchContainer, DispatchItem
from base import Base


class ReturnController(Base):

    def get_dispatch_container_instances_for_producer(self, using=None):
        """Returns a queryset of DoispatchContainer instances for this producer that are dispatched."""
        return DispatchContainer.objects.filter(producer=self.get_producer(), is_dispatched=True, return_datetime__isnull=True)

    def get_dispatched_item_instances_for_container(self, dispatch_container, using=None):
        """Returns a queryset of dispatched DispatchItem instances for this dispatch_container."""
        return DispatchItem.objects.filter(dispatch_container=dispatch_container, is_dispatched=True, return_datetime__isnull=True)

    def return_dispatched_items_for_container(self, dispatch_container, using=None):
        """Updates a queryset of dispatched DispatchItems to "no longer dispatched" for this dispatch_container."""
        #TODO: yes, this is inefficient. But can we check for just those items within this container efficiently?
        if self.has_outgoing_transactions():
            raise PendingTransactionError('Producer \'{0}\' has pending outgoing transactions on {1}. '
                                          'Run bhp_sync first.'.format(self.get_producer_name(), self.get_using_destination()))
        if self.has_incoming_transactions():
            raise PendingTransactionError('Producer \'{1}\' has pending incoming transactions on '
                                          'this server {0}. Consume them first.'.format(self.get_using_source(), self.get_producer_name()))
        # all tx's are consumed so flag as no longer dispatched
        item_count = DispatchItem.objects.using(using).filter(dispatch_container=dispatch_container, is_dispatched=True, return_datetime__isnull=True).count()
        #print [d.dispatch_container for d in DispatchItem.objects.using(using).filter(is_dispatched=True)]
        #print [d.pk for d in DispatchContainer.objects.all()]
        # TODO: 
        DispatchItem.objects.using(using).filter(dispatch_container=dispatch_container, is_dispatched=True, return_datetime__isnull=True).update(
            return_datetime=datetime.now(),
            is_dispatched=False)
        updated_item_count = DispatchItem.objects.using(using).filter(dispatch_container=dispatch_container, is_dispatched=True, return_datetime__isnull=True).count()
        print item_count, updated_item_count

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
        """Loops thru dispatch container instances for this producer and return them."""
        for dispatch_container in self.get_dispatch_container_instances_for_producer():
            print dispatch_container.pk
            self.return_dispatched_items_for_container(dispatch_container)
            self.return_dispatched_container(dispatch_container)
        return True
