import copy
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.core.exceptions import ImproperlyConfigured
from base_search import BaseSearch


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Search` objects. """
    
    SECTION_NAME = 0

    def __init__(self):
        self._registry = {}
        self.is_autodiscovered = False
        self._section_list = []

    def set_registry(self, search_cls):
        """Sets the dictionary to the controller register.

            Register format is {'<section_name>': (app_label, model_name)}.
            Attribute 'search_type' comes as a class attribute set on the base class. For example,
            SearchByWord.search_type = 'word'
        """
        if not issubclass(search_cls, BaseSearch):
            raise AlreadyRegistered('Expected an instance of BaseSearch.')
        if search_cls.section_name in self._registry:
            if search_cls.search_type == self.get(search_cls.section_name).search_type:
                raise AlreadyRegistered('A search class of type {0} is already registered for section {1}'.format(search_cls.search_type, search_cls.section_name))
        self._registry[search_cls.section_name] = search_cls

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

    def register(self, search_cls):
        if not search_cls.section_name:
            raise AttributeError('Attribute section_name cannot be None')
        if not search_cls.search_type:
            raise AttributeError('Attribute search_type cannot be None')
        if not search_cls.search_model:
            raise AttributeError('Attribute search_model cannot be None')
        if search_cls.section_name not in self._section_list:
            raise ImproperlyConfigured('{0} refers to section name {1} which is not a valid section. Must be any of {2}.'.format(search_cls, search_cls.section_name, self._section_list))
        self.set_registry(search_cls)

    def autodiscover(self, sections_list):
        self._section_list = [tpl[self.SECTION_NAME] for tpl in sections_list]
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(search._registry)
                import_module('%s.search' % app)
            except:
                search._registry = before_import_registry
                if module_has_submodule(mod, 'search'):
                    raise
        self.is_autodiscovered = True

search = Controller()
