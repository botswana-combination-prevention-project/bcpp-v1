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


class DispatchController(BaseDispatch):

    def __init__(self, using_source, producer=None, site_code=None, **kwargs):
        super(DispatchController, self).__init__(using_source, producer, site_code, **kwargs)
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

    def dispatch_as_json(self, export_instances, using_destination=None, **kwargs):
        """Serialize a remote model instance, deserialize and save to local instances.
            Args:
                remote_instance: a model instance from a remote server
                using: using parameter for the target server.
        """
        app_name = kwargs.get('app_name', None)
        if using_destination:
            if using_destination == 'default':
                # don't want to accidentally save to myself
                raise TypeError('Cannot export to database \'default\' (using).')
            if export_instances:
                if not isinstance(export_instances, (list, QuerySet)):
                    export_instances = [export_instances]
                json = serializers.serialize('json', export_instances, use_natural_keys=True)
                for obj_new in serializers.deserialize("json", json, use_natural_keys=True):
                    try:
                        obj_new.save(using=using_destination)
                    except IntegrityError:
                        if app_name:
                            # assume Integrity error is because of missing ForeignKey data
                            self._export_foreign_key_models(app_name)
                            # try again
                            obj_new.save(using=using_destination)
                        else:
                            raise
                    except:
                        raise
                    logger.info(obj_new.object)
