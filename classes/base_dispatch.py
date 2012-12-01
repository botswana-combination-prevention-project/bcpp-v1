import logging
import socket
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model, get_models, get_app, ForeignKey, OneToOneField
from bhp_visit.models import MembershipForm
from bhp_base_model.classes import BaseListModel
from base import Base

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatch(Base):

    def __init__(self, using_source, using_destination, site_code=None, **kwargs):
        super(BaseDispatch, self).__init(**kwargs)
        self.debug = kwargs.get('debug', False)
        self._producer = None
        self.set_using_source(using_source)
        self.set_using_destination(using_destination)
        self.set_producer()

    def set_dispatch_list(self, producer=None):
        """Sets the list of dispatched Dispatch model instances for the current producer."""
        Dispatch = get_model('bhp_dispatch', 'Dispatch')
        self._dispatch_list = Dispatch.objects.filter(
            producer=producer,
            is_checked_out=True,
            is_checked_in=False)

    def get_dispatch_list(self):
        """Returns the list of checked-out Dispatch model instances."""
        if not self._dispatch_list:
            self.set_dispatch_list(self.get_producer())
        return self._dispatch_list

    def set_producer(self):
        """Sets the instance of the current producer and updates the list checked-out Dispatch models.

        .. note:: The producer must always exist on the source. If dispatching via the device, try to
                  find a producer with the settings_key of the format ``DEVICE_HOSTNAME-DBNAME``
                  where DBNAME is the NAME attribute of the ``default`` DATABASE on the device."""
        Producer = get_model('bhp_sync', 'Producer')
        # try to determine producer from using_destination
        if self.get_using_destination() == 'default':
            # try to find the producer on the server with hostname + database name
            settings_key = '{0}-{1}'.format(socket.gethostname().lower(), settings.DATABASES.get('default').get('NAME'))
            if Producer.objects.using(self.get_using_source()).filter(settings_key=settings_key).exists():
                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=settings_key)
        else:
            if Producer.objects.using(self.get_using_source()).filter(settings_key=self.get_using_destination()).exists():
                self._producer = Producer.objects.using(self.get_using_source()).get(settings_key=self.get_using_destination())
        if not self._producer:
            raise TypeError('Dispatcher cannot find producer with settings key {0} on the source {1}.'.format(self.get_using_destination(), self.get_using_source()))
        # check the producers DATABASES key exists
        # TODO: what if producer is "me", e.g settings key is 'default'
        settings_key = self._producer.settings_key
        if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == settings_key]:
            raise ImproperlyConfigured('Dispatcher expects settings attribute DATABASES to have a NAME '
                                       'key to the \'producer\'. Got name=\'{0}\', settings_key=\'{1}\'.'.format(self._producer.name, self._producer.settings_key))
        # producer has changed so update the list of
        # dispatched Dispatch items instances for this producer
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
        BaseVisitTracking = get_model('bhp_visit_tracking', 'BaseVisitTracking')
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
        """Updates all list models on the destination with data from the source.
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
                list_model.objects.using(self.get_using_source()).all().order_by('name'),
                use_natural_keys=True
                )

            for obj in serializers.deserialize("json", json):
                obj.save(using=self.get_using_destination())
