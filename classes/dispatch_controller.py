import logging
from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import get_models, get_app, ForeignKey, OneToOneField
from bhp_sync.models import Producer
from bhp_visit.models import MembershipForm
from bhp_visit_tracking.models import BaseVisitTracking

from bhp_base_model.classes import BaseListModel
from bhp_dispatch.models import Dispatch, DispatchItem


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class DispatchController(object):

    VISIT_MODEL_FLD = 0
    VISIT_MODEL_CLS = 1

    def __init__(self, using_source, producer=None, site_code=None, **kwargs):
        self._dispatch_list = []
        self.debug = kwargs.get('debug', False)
        self._producer = None
        self._using_source = None
        self.set_using_source(using_source)
        self.set_producer(producer)

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

#    def fetch_study_site(self, site_code):
#        if not site_code:
#            raise ValueError("Please specify the site code!")
#
#        try:
#            site = StudySite.objects.get(site_code=site_code)
#            self.dispatch_as_json(site, self.get_producer())
#        except ObjectDoesNotExist:
#            raise ValueError("No Site was found with site code {0}. I'm " \
#                             "therefore killing myself!".format(site_code))

    def set_using_source(self, using_source=None):
        if not using_source:
            raise TypeError('Parameter \'using_source\' cannot be None.')
        if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == using_source]:
            raise ImproperlyConfigured('Dispatcher expects settings attribute DATABASES to have a NAME key to the \'source\'. Got \'{0}\'.'.format(using_source))
        self._using_source = using_source

    def get_using_source(self):
        if not self._using_source:
            self.set_using_source()
        return self._using_source

    def set_dispatch_list(self, producer=None):
        """Sets the list of checked-out Dispatch model instances for the current producer."""
        if not producer:
            producer = self.get_producer()
        self._dispatch_list = Dispatch.objects.filter(
            producer=producer,
            is_checked_out=True,
            is_checked_in=False)

    def get_dispatch_list(self):
        """Returns the list of checked-out Dispatch model instances."""
        if not self._dispatch_list:
            self.set_dispatch_list()
        return self._dispatch_list

    def set_producer(self, producer_name=None):
        """Sets to the instance of the current producer and updates the list checked-out Dispatch models."""
        if not producer_name:
            raise TypeError("Parameter \'producer_name\' cannot be None.")
        # does this producer exist on the source?
        if not Producer.objects.using(self.get_using_source()).filter(name=producer_name).exists():
            raise TypeError('Dispatcher cannot find producer {0} on the source {1}.'.format(producer_name, self.get_using_source()))
        # TODO: should this be name or instance??
        self._producer = Producer.objects.using(self.get_using_source()).get(name=producer_name)
        # check the producers DATABASES key exists
        # TODO: what if producer is "me", e.g settings key is 'default'
        settings_key = self._producer.settings_key
        if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == settings_key]:
            raise ImproperlyConfigured('Dispatcher expects settings attribute DATABASES to have a NAME key to the \'producer\'. Got \'{0}\'.'.format(producer_name))
        # producer has changed so update the list of checked-out Dispatch instances for this producer
        self.set_dispatch_list(self._producer)

    def get_producer(self):
        """Returns an instance of the current producer."""
        if not self._producer:
            self.set_producer()
        return self._producer

    def get_membershipform_models(self):
        return [membership_form.content_type_map.content_type.model_class() for membership_form in MembershipForm.objects.all()]

    def set_visit_model_cls(self, app_name, model_cls):
        """Sets the visit_model_cls attribute with a dictionary of tuples (field name, class) by app.
        """
        self._visit_models = {}
        if not model_cls:
            raise TypeError('Parameter model_cls cannot be None.')
        for field in model_cls._meta.fields:
            if isinstance(field, ForeignKey, OneToOneField):
                field_cls = field.rel.to
                if issubclass(field_cls, BaseVisitTracking):
                    # does this dict ever have more than one entry??
                    self._visit_models.update({app_name: (field.name, field_cls)})

    def get_visit_model_cls(self, app_name, model_cls=None, **kwargs):
        """Returns a tuple of (field name, class) or just one of the tuple items.

        Keywords:
            key: either 'name' or 'cls'. If specified, only returns the item in the tuple instead of the whole tuple.
        """
        if not self._visit_models:
            self.set_visit_models(app_name, model_cls)
        # check for kwarg 'key' and set key to 0 or 1 (or None if not found)
        key = {'name': 0, 'cls': 1}.get(kwargs.get('key', None), None)
        if not self.visit_models.get(app_name):
            tpl = (None, None)
        else:
            tpl = self._visit_models.get(app_name)
        if key:
            return tpl[key]
        else:
            return tpl

    def _export_foreign_key_models(self, app_name):
        """Finds foreignkey model classes other than the visit model class and exports the instances."""
        list_models = []
        if not app_name:
            raise TypeError('Parameter app_name cannot be None.')
        app = get_app(app_name)
        for model_cls in get_models(app):
            visit_field_name = self._get_visit_model_cls(app_name, model_cls, key='name')
            if getattr(model_cls, visit_field_name, None):
                for field in model_cls._meta.fields:
                    if not field.name == visit_field_name and isinstance(field, (ForeignKey, OneToOneField)):
                        field_cls = field.rel.to
                        if field_cls not in list_models:
                            list_models.append(field_cls)
        for model_cls in list_models:
            self.dispatch_as_json(model_cls.objects.all(), self.get_producer(), app_name=app_name)

    def get_scheduled_models(self, app_name):
        """Returns a list of model classes with a foreign key to the visit model for the given app, excluding audit models."""
        app = get_app(app_name)
        scheduled_models = []
        for model_cls in get_models(app):
            field_name, visit_model_cls = self._get_visit_model_cls(app_name, model_cls)
            if visit_model_cls:
                if getattr(model_cls, field_name, None):
                    if not model_cls._meta.object_name.endswith('Audit'):
                        scheduled_models.append(model_cls)
        return scheduled_models

    def update_lists(self):
        """Update all list models in "default" with data from "server".
        """
        #Make sure we have a target producer to export lists to
        if not self.get_producer():
            raise ValueError("PLEASE specify the producer you want checkout models to!")
        list_models = []
        for model in get_models():
            if issubclass(model, BaseListModel):
                list_models.append(model)
        for list_model in list_models:
            logger.info(list_model._meta.object_name)
            json = serializers.serialize(
                'json',
                list_model.objects.all().order_by('name'),
                use_natural_keys=True
                )

            for obj in serializers.deserialize("json", json):
                obj.save(using=self.get_producer().settings_key)

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
