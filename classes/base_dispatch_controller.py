import logging
from datetime import datetime
from django.core import serializers
from django.db import IntegrityError
from django.db.models import get_model
from django.db.models.query import QuerySet
from bhp_dispatch.models import DispatchItem
from bhp_dispatch.exceptions import DispatchError
from base_dispatch import BaseDispatch


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatchController(BaseDispatch):

    def __init__(self, using_source, using_destination, **kwargs):
        super(BaseDispatchController, self).__init__(using_source, using_destination, **kwargs)
        self._dispatch_list = []

    def return_all(self):
        """Returns all Dispatched by flagging :attr:`is_dispatched` = False.

        .. note::
           This will be called after all the transactions for the producer have been consumed
           therefore, we can assume that the information that was dispatch to the producer
           has been sent to server; hence, we mark all the dispatch items as checked in
        """
        # TODO: confirm all transactions have been consumed?

        # Find all dispatch for the given producer that have not been checked in
        for dispatch in self.get_dispatch_list():
            self.return_from_dispatch(dispatch)

    def return_from_dispatch(self, dispatch):
        """Flags all items in a Dispatch as returned and then flags the Dispatch as returned."""
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        if dispatch:
            item_identifiers = dispatch.dispatch_items.split()
            for item_identifier in item_identifiers:
                item = DispatchItem.objects.get(
                    producer=dispatch.producer,
                    item_identifier=item_identifier,
                    is_dispatched=True)
                item.is_dispatched = False
                item.return_datetime = datetime.today()
                item.save()
            dispatch.is_dispatched = False
            dispatch.return_datetime = datetime.today()
            dispatch.save()

