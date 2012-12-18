import logging
from django.db.models import get_model, get_models, get_app, ForeignKey, OneToOneField
from bhp_visit.models import MembershipForm
from base import Base

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseDispatch(Base):

    def __init__(self, using_source, using_destination, **kwargs):
        super(BaseDispatch, self).__init__(using_source, using_destination, **kwargs)
        self.debug = kwargs.get('debug', False)

    def set_dispatch_list(self, producer=None):
        """Sets the list of dispatched Dispatch model instances for the current producer."""
        Dispatch = get_model('bhp_dispatch', 'Dispatch')
        self._dispatch_list = Dispatch.objects.using(self.get_using_source()).filter(
            producer=producer,
            is_dispatched=True)

    def get_dispatch_list(self):
        """Returns the list of checked-out Dispatch model instances."""
        if not self._dispatch_list:
            self.set_dispatch_list(self.get_producer())
        return self._dispatch_list

    def set_producer(self):
        super(BaseDispatch, self).set_producer()
        # producer has changed so update the list of
        # dispatched Dispatch items instances for this producer
        self.set_dispatch_list(self._producer)

    def get_membershipform_models(self):
        """Returns a list of 'visible' membership form model classes."""
        return [membership_form.content_type_map.content_type.model_class() for membership_form in MembershipForm.objects.using(self.get_using_source()).filter(visible=True)]

    def set_visit_model_cls(self, app_name, model_cls):
        """Sets the visit_model_cls attribute with a dictionary of tuples (field name, class) by app.
        """
        from bhp_visit_tracking.models import BaseVisitTracking
        self._visit_models = {}
        if not model_cls:
            raise TypeError('Parameter model_cls cannot be None.')
        for field in model_cls._meta.fields:
            if isinstance(field, (ForeignKey, OneToOneField)):
                field_cls = field.rel.to
                if issubclass(field_cls, BaseVisitTracking):
                    # does this dict ever have more than one entry??
                    self._visit_models.update({app_name: (field.name, field_cls)})

    def get_visit_model_cls(self, app_name, model_cls=None, **kwargs):
        """Returns a tuple of (field name, class) or just one of the tuple items.

        Keywords:
            index: either 'name' or 'cls'. If specified, only returns the item in the tuple instead of the whole tuple.
        """
        if not self._visit_models.get(app_name):
            self.set_visit_model_cls(app_name, model_cls)
        # check for kwarg 'key' and set key to 0 or 1 (or None if not found)
        index = {'name': 0, 'cls': 1}.get(kwargs.get('index', None), None)
        if not self._visit_models.get(app_name):
            tpl = (None, None)
        else:
            tpl = self._visit_models.get(app_name)
        if index in [0, 1]:
            return tpl[index]
        else:
            return tpl

    def dispatch_foreign_key_instances(self, app_name):
        """Finds foreign_key model classes other than the visit model class and exports the instances."""
        list_models = []
        if not app_name:
            raise TypeError('Parameter app_name cannot be None.')
        app = get_app(app_name)
        for model_cls in get_models(app):
            # TODO: this could be wrong visit_field_name?
            visit_field_name = self.get_visit_model_cls(app_name, model_cls, index='name')
            if getattr(model_cls, visit_field_name, None):
                for field in model_cls._meta.fields:
                    if not field.name == visit_field_name and isinstance(field, (ForeignKey, OneToOneField)):
                        field_cls = field.rel.to
                        if field_cls not in list_models:
                            list_models.append(field_cls)
        logger.info('Ready to dispatch foreign keys: {0}'.format(list_models))
        for model_cls in list_models:
            self.dispatch_as_json(model_cls.objects.using(self.get_using_source()).all(), app_name=app_name)

    def get_scheduled_models(self, app_name=None):
        """Returns a list of model classes with a foreign key to the visit model for the given app, excluding audit models."""
        for app_name in self.get_dispatch_app_name():
            app = get_app(self.get_dispatch_app_name())
            scheduled_models = []
            for model_cls in get_models(app):
                field_name, visit_model_cls = self.get_visit_model_cls(app_name, model_cls)
                if visit_model_cls:
                    if getattr(model_cls, field_name, None):
                        if not model_cls._meta.object_name.endswith('Audit'):
                            scheduled_models.append(model_cls)
        return scheduled_models

#    def update_lists(self):
#        """Updates all list models on the destination with data from the source.
#        """
#        #Make sure we have a target producer to export lists to
#        if not self.get_producer():
#            raise ValueError("PLEASE specify the producer you want checkout models to!")
#        list_models = []
#        for model in get_models():
#            if issubclass(model, BaseListModel):
#                list_models.append(model)
#        for list_model in list_models:
#            logger.info(list_model._meta.object_name)
#            json = serializers.serialize(
#                'json',
#                list_model.objects.using(self.get_using_source()).all().order_by('name'),
#                use_natural_keys=True
#                )
#
#            for obj in serializers.deserialize("json", json):
#                obj.save(using=self.get_using_destination())
