import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from base_search import BaseSearch


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Search` objects. """

    def __init__(self):
        self._registry = {}

    def set_registry(self, search_cls):
        if not issubclass(search_cls, BaseSearch):
            raise AlreadyRegistered('Expected an instance of BaseSearch.')
        if search_cls.search_type in self._registry:
            raise AlreadyRegistered('A search class of type {1} is already registered ({0})'.format(search_cls, search_cls.search_type))
        self._registry[search_cls.search_type] = search_cls

    def get(self, search_type):
        return self._registry.get(search_type)

    def get_registry(self, search_type=None):
        if search_type:
            if search_type in self._registry:
                return self._registry.get(search_type)
            else:
                return {}
        return self._registry

    def register(self, search_cls):
        if not search_cls.search_type:
            raise AttributeError('Attribute search_type cannot be None')
        self.set_registry(search_cls)

    def autodiscover(self):
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(search._registry)
                import_module('%s.search' % app)
            except:
                search._registry = before_import_registry
                if module_has_submodule(mod, 'search'):
                    raise
search = Controller()
