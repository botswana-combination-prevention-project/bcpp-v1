import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class SiteLabTracker(object):
    """Registers from modules with a lab_tracker module (lab_tracker.py)."""
    def __init__(self):
        self._registry = []

    def register(self, lab_tracker_cls):
        if lab_tracker_cls in self._registry:
            raise AlreadyRegistered('The class %s is already registered' % lab_tracker_cls)
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
