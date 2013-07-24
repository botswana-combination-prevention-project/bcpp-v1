import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from bhp_map.exceptions import MapperError
from mapper import Mapper


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
        # use map_area class attribute add the dictionary key
        if mapper_cls.map_area in self._registry:
            raise AlreadyRegistered('The mapper class {0} is already registered ({1})'.format(mapper_cls, mapper_cls.map_area))
        self._registry[mapper_cls.map_area] = mapper_cls

    def get(self, name):
        return self._registry.get(name)

    def get_registry(self, name=None):
        if name:
            if name in self._registry:
                return self._registry.get(name)
            else:
                raise MapperError('{0} is not a valid mapper name in {1}.'.format(name, self._registry))
        return self._registry

    def get_mapper_as_tuple(self):
        lst = [k for k in self._registry]
        lst.sort()
        return [(l, l) for l in lst]

    def register(self, mapper_cls):
        self.set_registry(mapper_cls)

    def autodiscover(self):
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(site_mappers._registry)
                import_module('%s.mappers' % app)
            except:
                site_mappers._registry = before_import_registry
                if module_has_submodule(mod, 'mappers'):
                    raise
site_mappers = Controller()
