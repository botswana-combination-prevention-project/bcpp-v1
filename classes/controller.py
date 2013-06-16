import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from base_section_view import BaseSectionView


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Section` objects. """

    def __init__(self):
        self._registry = {}

    def set_registry(self, section_view_cls):
        if not issubclass(section_view_cls, BaseSectionView):
            raise AlreadyRegistered('Expected an instance of BaseSectionView.')
        if section_view_cls.section_name in self._registry:
            raise AlreadyRegistered('A section view class of type {1} is already registered ({0})'.format(section_view_cls, section_view_cls.section_name))
        self._registry[section_view_cls.section_name] = section_view_cls

    def get(self, section_name):
        return self._registry.get(section_name)

    def get_registry(self, section_name=None):
        if section_name:
            if section_name in self._registry:
                return self._registry.get(section_name)
            else:
                return {}
        return self._registry

    def all(self):
        return self.get_registry()

    def get_section_names(self):
        return self._registry().keys()

    def register(self, section_view_cls):
        if not section_view_cls.section_name:
            raise AttributeError('Attribute section_name cannot be None')
        self.set_registry(section_view_cls)

    def autodiscover(self):
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(site_sections._registry)
                import_module('%s.section' % app)
            except:
                site_sections._registry = before_import_registry
                if module_has_submodule(mod, 'section'):
                    raise
site_sections = Controller()
