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

    def __init__(self):
        self._registry = {}
        self.is_autodiscovered = False
        self._section_list = None

    def register(self, search_cls):
        self.set_registry(search_cls)

    def set_registry(self, search_cls):
        """Sets the dictionary to the controller register.

            Register format is {'<section_name>': (app_label, model_name)}.
            Attribute 'search_type' comes as a class attribute set on the base class. For example,
            SearchByWord.search_type = 'word'
        """
        if not issubclass(search_cls, BaseSearch):
            raise AlreadyRegistered('Expected an instance of BaseSearch.')
        if not search_cls.search_type:
            raise AttributeError('Attribute search_type cannot be None')
        if not search_cls.search_model:
            raise AttributeError('Attribute search_model cannot be None')
        if not search_cls.section:
            raise ImproperlyConfigured('Class attribute section may not be None for search class {0}. Expected a subclass of BaseSectionView.'.format(search_cls))
        section = search_cls.section()
        if section.get_section_name() in self._registry:
            raise AlreadyRegistered('A search class {0} is already registered for section {1}'.format(search_cls, section.get_section_name()))
        self._registry[section.get_section_name()] = search_cls

    def get(self, section_name):
        return self._registry.get(section_name)

    def get_registry(self, section_name=None):
        if section_name:
            if not section_name in self._registry:
                raise TypeError('Invalid section name. Got {0}. Expected any of {1}'.format(section_name, self.get_section_names()))
            return self._registry.get(section_name)
        return self._registry

    def set_section_list(self):
        self._section_list = [cls.section_name for cls in self._registry.itervalues()]

    def get_section_list(self):
        if not self._section_list:
            self.set_section_list()
        return self._section_list

    def all(self):
        return self.get_registry()

    def autodiscover(self, section_name_list):
        """Discovers search classes in each installed app with a search.py.

        By default this is called by :func:`setup` in :class:`bhp_sections.classes.BaseSectionIndexView`.

        Otherwise you need to call something like this::

            site_search.autodiscover(site_sections.get_section_list())"""
        if not self.is_autodiscovered:
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_search._registry)
                    import_module('%s.search' % app)
                except:
                    site_search._registry = before_import_registry
                    if module_has_submodule(mod, 'search'):
                        raise
            self.is_autodiscovered = True

site_search = Controller()
