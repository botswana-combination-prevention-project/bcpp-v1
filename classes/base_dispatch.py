import logging
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_models, get_app, ForeignKey, OneToOneField
from bhp_sync.models import Producer
from bhp_visit.models import MembershipForm
from bhp_visit_tracking.models import BaseVisitTracking
from bhp_base_model.classes import BaseListModel


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatch(object):

    def __init__(self, using_source, producer=None, site_code=None, **kwargs):
        self.debug = kwargs.get('debug', False)
        self._producer = None
        self._using_source = None
        self.set_using_source(using_source)
        self.set_producer(producer)

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
