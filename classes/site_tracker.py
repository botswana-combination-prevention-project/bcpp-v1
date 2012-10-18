import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class SiteTracker(object):
    """Registers tuples of (model_cls, history) from modules with a tracker module (tracker.py)."""
    def __init__(self):
        self._registry = {}

    def register(self, model_cls, history):
        """Registers tuples of (model_cls, history) from modules with a tracker module (tracker.py).

            Args:
                model_cls: a model class that """
        if model_cls._meta.object_name in self._registry.keys():
            if self._registry[model_cls._meta.object_name] == (model_cls, history):
                raise AlreadyRegistered('The class %s is already registered' % model_cls._meta.object_name)
        self._registry[model_cls._meta.object_name] = (model_cls, history)

    def get(self, key):
        return self._registry.get(key)

    def iteritems(self):
        return self._registry.iteritems

    def autodiscover(self):
        """Discovers tracker modules in your apps."""
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(tracker._registry)
                import_module('%s.tracker' % app)
            except:
                tracker._registry = before_import_registry
                if module_has_submodule(mod, 'tracker'):
                    raise
# A global to contain all tracker instances from modules
tracker = SiteTracker()
