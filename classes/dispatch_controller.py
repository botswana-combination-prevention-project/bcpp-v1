import logging
from datetime import datetime
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import get_models, get_app, ForeignKey, OneToOneField
from bhp_visit.models import MembershipForm
from bhp_variables.models import StudySite
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

    def __init__(self, debug=False, producer=None, site_code=None):
        self.dispatch_list = []
        self.debug = debug
        self.producer = None
        if producer:
            self.set_producer(producer)

    def checkin(self, dispatch):
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

    def fetch_study_site(self, site_code):
        if not site_code:
            raise ValueError("Please specify the site code!")

        try:
            site = StudySite.objects.get(site_code=site_code)
            self.dispatch_as_json(site, self.get_producer())
        except ObjectDoesNotExist:
            raise ValueError("No Site was found with site code {0}. I'm " \
                             "therefore killing myself!".format(site_code))

    def get_dispatch_list(self):
        return self.dispatch_list

    def set_producer(self, producer=None):
        if producer:
            self.producer = producer
        else:
            raise ValueError("PLEASE specify the producer you want checkout models to!")

    def get_producer(self):
        if not self.producer:
            self.set_producer()
        return self.producer

    def checkin_all(self):
        """Updates all the Household dispatches and dispatch items as checked back in.

        .. note::
           This will called after all the transaction for the producer have been consumed
           therefore, we can assume that the information that was dispatch to the producer
           has been sent to server; hence, we mark all the dispatch items a checked in
        """
        # Find all dispatch for the given producer that have not been checked in
        for dispatch in self.dispatch_list:
            self.checkin(dispatch)

    def update_checkedout_dispatches(self):
        """Returns all dispatched items for the current producer -- those that are checked out."""
        self.dispatch_list = Dispatch.objects.filter(
            producer=self.get_producer(),
            is_checked_out=True,
            is_checked_in=False
            )

    def get_membership_form_models(self):
        _models = []
        for membership_form in MembershipForm.objects.all():
            _models.append(membership_form.content_type_map.content_type.model_class())
        return _models

    def _get_visit_model_cls(self, app_name, model_cls=None):
        if not self.visit_models.get(app_name):
            self._set_visit_model_cls(app_name, model_cls)
        if not self.visit_models.get(app_name):
            return (None, None)
        return self.visit_models.get(app_name)

    def _export_foreign_key_models(self, app_name):
        """Finds foreignkey model classes other than the visit model class and exports the instances."""
        list_models = []
        if not app_name:
            raise TypeError('Parameter app_name cannot be None.')
        app = get_app(app_name)
        for model_cls in get_models(app):
            visit_field_name, visit_model_cls = self._get_visit_model_cls(app_name, model_cls)
            if getattr(model_cls, visit_field_name, None):
                for field in model_cls._meta.fields:
                    if not field.name == visit_field_name and isinstance(field, (ForeignKey, OneToOneField)):
                        field_cls = field.rel.to
                        if field_cls not in list_models:
                            list_models.append(field_cls)
        for model_cls in list_models:
            self.dispatch_as_json(model_cls.objects.all(), self.producer, app_name=app_name)

    def _get_scheduled_models(self, app_name):
        """Returns a list of model classes with a key to SubjectVisit excluding audit models."""
        app = get_app(app_name)
        # self._export_foreign_key_models(self, app_name)
        subject_model_cls = []
        for model_cls in get_models(app):
            field_name, visit_model_cls = self._get_visit_model_cls(app_name, model_cls)
            if visit_model_cls:
                if getattr(model_cls, field_name, None):
                    if not model_cls._meta.object_name.endswith('Audit'):
                        subject_model_cls.append(model_cls)
        return subject_model_cls

    def update_lists(self):
        """Update all list models in "default" with data from "server".
        """
        #Make sure we have a target producer to export lists to
        if not self.producer:
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
                obj.save(using=self.producer)

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
