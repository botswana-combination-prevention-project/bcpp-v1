import copy
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class SiteLabTracker(object):
    """Registers from modules with a lab_tracker module (lab_tracker.py).

    Models in the models tuples class attribute
      1. must define the method :func:`get_subject_identifier`.
      2. may define:
           * :func:`get_result_value(attr)`
           * :func:`get_result_datetime(attr)`
    """
    def __init__(self):
        self._registry = []

    def register(self, lab_tracker_cls):
        if lab_tracker_cls in self._registry:
            raise AlreadyRegistered('The class %s is already registered' % lab_tracker_cls)
        # confirm the models in the models class attribute have the required methods.
        if 'models' in dir(lab_tracker_cls):
            for model, value_attr, date_attr in lab_tracker_cls.models:
                if 'get_subject_identifier' not in dir(model):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. Define the method \'get_subject_identifier()\' on the model first.'.format(model._meta.object_name))
                if 'get_result_value' not in dir(model):
                    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. Define the method \'get_result_value()\' on the model first.'.format(model._meta.object_name))
                #if 'get_result_datetime' not in dir(model):
                #    raise ImproperlyConfigured('Model {0} cannot be registered to a lab tracker. Define the method \'get_result_datetime()\' on the model first.'.format(model._meta.object_name))
                # add ResultItem to the models
        else:
            lab_tracker_cls.models = []
        lab_tracker_cls.models.append(lab_tracker_cls.result_item_tpl)
        self._registry.append(lab_tracker_cls)

    def all(self):
        return self._registry

    def autodiscover(self):
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(lab_tracker._registry)
                import_module('%s.lab_tracker' % app)
            except:
                lab_tracker._registry = before_import_registry
                if module_has_submodule(mod, 'lab_tracker'):
                    raise
# A global to contain all tracker instances from modules
lab_tracker = SiteLabTracker()
