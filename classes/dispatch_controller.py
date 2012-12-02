import logging
from datetime import datetime
from django.core import serializers
from django.db import IntegrityError
from django.db.models import get_model
from django.db.models.query import QuerySet
from base_dispatch import BaseDispatch


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatchController(BaseDispatch):

    def __init__(self, using_source, producer=None, site_code=None, **kwargs):
        super(BaseDispatchController, self).__init__(using_source, producer, site_code, **kwargs)
        self._dispatch_list = []

    def checkin_all(self):
        """Updates all the dispatches and dispatch items as checked back in.

        .. note::
           This will be called after all the transactions for the producer have been consumed
           therefore, we can assume that the information that was dispatch to the producer
           has been sent to server; hence, we mark all the dispatch items as checked in
        """
        # TODO: confirm all transactions have been consumed?

        # Find all dispatch for the given producer that have not been checked in
        for dispatch in self.get_dispatch_list():
            self.checkin_dispatched_items(dispatch)

    def checkin_dispatched_items(self, dispatch):
        """Updates a Item dispatch and dispatch items as checked back in.
        """
        DispatchItem = get_model('bhp_dispatch', 'DispatchItem')
        if dispatch:
            item_identifiers = dispatch.checkout_items.split()
            for item_identifier in item_identifiers:
                item = DispatchItem.objects.get(
                    producer=dispatch.producer,
                    item_identifier=item_identifier,
                    is_checked_out=True,
                    is_checked_in=False
                    )
                    #Update each item as checked in, and checked in today
                item.is_checked_in = True
                item.datetime_checked_in = datetime.today()
                item.save()
                # Now about the the dispatch
            dispatch.is_checked_in = True
            dispatch.datetime_checked_in = datetime.today()
            dispatch.save()

    def dispatch_as_json(self, source_instances, **kwargs):
        """Serialize a remote model instance, deserialize and save to local instances.

            Args:
                source_instance: a model instance(s) from the source server
                using: `using` parameter for the destination device.
            Keywords:
                app_name: app name for instances
        """
        app_name = kwargs.get('app_name', None)
        if source_instances:
            if not isinstance(source_instances, (list, QuerySet)):
                source_instances = [source_instances]
            json = serializers.serialize('json', source_instances, use_natural_keys=True)
            for obj_new in serializers.deserialize("json", json, use_natural_keys=True):
                try:
                    obj_new.save(using=self.get_using_destination())
                except IntegrityError:
                    if not app_name:
                        app_name = source_instances[0]._meta.app_label
                    # assume Integrity error was because of missing ForeignKey data
                    self.dispatch_foreign_key_instances(app_name)
                    # try again
                    obj_new.save(using=self.get_using_destination())
                except:
                    raise
                logger.info(obj_new.object)
