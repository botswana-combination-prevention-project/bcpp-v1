import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from bhp_map.exceptions import MapperError
from _mapper import Mapper


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Mapping` objects. """

    def __init__(self):
        self._registry = {}

    def set_registry(self, mapper_cls):
        if not issubclass(mapper_cls, Mapper):
            raise MapperError('Expected a subclass of Mapper.')
        if mapper_cls.search_label in self._registry:
            raise AlreadyRegistered('The mapper class {0} is already registered ({1})'.format(mapper_cls, mapper_cls.name))
        self._registry[mapper_cls.name] = mapper_cls

    def get(self, name):
        return self._registry.get(name)

    def get_registry(self, name=None):
        if name:
            if name in self._registry:
                return self._registry.get(name)
            else:
                return {}
        return self._registry

    def register(self, mapper_cls):
        if not mapper_cls.name:
            raise AttributeError('Mapper attribute name cannot be None')
        self.set_registry(mapper_cls)

    def autodiscover(self):
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(mapper._registry)
                import_module('%s.mappers' % app)
            except:
                mapper._registry = before_import_registry
                if module_has_submodule(mod, 'mappers'):
                    raise
mapper = Controller()
