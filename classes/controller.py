import copy
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from base_section_view import BaseSectionView
from helpers import SectionNamedTpl


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Section` objects. """

    def __init__(self):
        self._registry = {}
        self.is_autodiscovered = False
        self._section_tuples = None
        self._section_names = None
        self._section_display_names = None
        self._section_display_indexes = None
        self._indexed_section_tuples = None
        self._indexed_section_display_names = None

    def reset_controller(self):
        """Resets everything except the registry."""
        self._section_tuples = None
        self._section_names = None
        self._section_display_names = None
        self._section_display_indexes = None
        self._indexed_section_tuples = None
        self._indexed_section_display_names = None

    def register(self, section_view_cls):
        """Registers section_view_classes to the registry dictionary as {section_view_cls.sectionname: section_view_cls}."""
        self.set_registry(section_view_cls)

    def set_registry(self, section_view_cls):
        if not issubclass(section_view_cls, BaseSectionView):
            raise AlreadyRegistered('Expected an instance of BaseSectionView. Got {0}.'.format(section_view_cls))
        if not section_view_cls.section_name:
            raise AttributeError('Attribute section_name cannot be None for class {0}'.format(section_view_cls))
        if section_view_cls.section_name in self._registry:
            raise AlreadyRegistered('A section view class of type {1} is already registered ({0})'.format(section_view_cls, section_view_cls.section_name))
        self._registry[section_view_cls().get_section_name()] = section_view_cls

    def get(self, section_name):
        """Returns a dictionary value, s section_view_cls, for the given section name."""
        if not section_name in self._registry:
            raise TypeError('Invalid section name. Got {0}. Expected any of {1}'.format(section_name, self.get_section_names()))
        return self._registry.get(section_name)

    def get_registry(self, section_name=None):
        if section_name:
            return self.get(section_name)
        return self._registry

    def all(self):
        """Returns the registry as a dcitionary."""
        return self.get_registry()

    def set_section_names(self):
        """Sets to a list of the internal section names, the same as the _registry keys."""
        self._section_names = [tpl.section_name for tpl in self.get_section_tuples()]
        self._section_names.sort()

    def get_section_names(self):
        if not self._section_names:
            self.set_section_names()
        return self._section_names

    def set_indexed_section_tuples(self):
        self._indexed_section_tuples = []
        for index in self.get_section_display_indexes():
            for section_tpl in self.get_section_tuples():
                if section_tpl.display_index == index:
                    self._indexed_section_tuples.append(section_tpl)
                    break

    def get_indexed_section_tuples(self):
        """Returns a list of section tuples in order of display index."""
        if not self._indexed_section_tuples:
            self.set_indexed_section_tuples()
        return self._indexed_section_tuples

    def set_indexed_section_display_names(self):
        self._indexed_section_display_names = [tpl.display_name for tpl in self.get_indexed_section_tuples()]

    def get_indexed_section_display_names(self):
        if not self._indexed_section_display_names:
            self.set_indexed_section_display_names()
        return self._indexed_section_display_names

    def set_section_display_names(self):
        self._section_display_names = [tpl.display_name for tpl in self.get_section_tuples()]
        self._section_display_names.sort()

    def get_section_display_names(self):
        if not self._section_display_names:
            self.set_section_display_names()
        return self._section_display_names

    def set_section_display_indexes(self):
        """Sets a ordered list of section display indexes."""
        self._section_display_indexes = [tpl.display_index for tpl in self.get_section_tuples()]
        self._section_display_indexes.sort()
        # check for duplicates
        lst = list(set(self._section_display_indexes))
        lst.sort()
        if lst != self._section_display_indexes:
            raise ImproperlyConfigured('Section classes must have a unique section_display_index. '
                                       'Got {0} from site_sections {1}. Check the section cls in '
                                       'each app. Section tuples are {2}'.format(self._section_display_indexes, site_sections.get_section_names(), site_sections.get_section_tuples()))

    def get_section_display_indexes(self):
        """Returns an ordered list of section display indexes."""
        if not self._section_display_indexes:
            self.set_section_display_indexes()
        return self._section_display_indexes

    def set_section_tuples(self):
        """Sets to a list of named tuples with section information of the format (section_name, display_name, display_index)."""
        self._section_tuples = []
        for cls in self.get_registry().itervalues():
            inst = cls()
            tpl = SectionNamedTpl(section_name=inst.get_section_name(), display_name=inst.get_section_display_name(), display_index=inst.get_section_display_index())
            if tpl not in self._section_tuples:
                self._section_tuples.append(tpl)
        return self._section_tuples

    def get_section_tuples(self):
        """Returns a list of named tuples (section_name, display_name, display_index)."""
        if not self._section_tuples:
            self.set_section_tuples()
        return self._section_tuples

    def get_section_list(self):
        """Wrapper for :func:`get_section_tuples`."""
        return self.get_section_tuples()

    def unregister(self, section_name):
        if section_name in self.get_registry():
            del self._registry[section_name]
        self.reset_controller()

    def autodiscover(self):
        if not self.is_autodiscovered:
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_sections._registry)
                    import_module('%s.section' % app)
                except:
                    site_sections._registry = before_import_registry
                    if module_has_submodule(mod, 'section'):
                        raise
            self.is_autodiscovered = True

site_sections = Controller()
