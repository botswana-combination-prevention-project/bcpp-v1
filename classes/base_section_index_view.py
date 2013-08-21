from controller import site_sections
from bhp_search.classes import site_search


class BaseSectionIndexView(object):

    """ Base section class. """

    def __init__(self):
        """
        Keyword Arguments:
            search_result_template --
            section_name --
        """
        self._indexed_section_tuples = None
        self._section_name_list = None
        self._section_display_name_list = None
        self._indexed_section_display_name_list = None
        self.selected_section = None
        self.is_setup = False

    def setup(self):
        if not self.is_setup:
            site_sections.autodiscover()
            self.set_indexed_section_tuples()
            site_search.autodiscover(self.get_section_name_list())
            self.is_setup = True

    def set_indexed_section_tuples(self):
        """ Sets an ordered (by display index) list of section tuples that apply to this section class' urlpatterns."""
        self._indexed_section_tuples = site_sections.get_indexed_section_tuples()

    def get_section_tuples(self):
        return self.get_indexed_section_tuples()

    def get_section_list(self):
        return self.get_indexed_section_tuples()

    def get_indexed_section_tuples(self):
        """Returns a list of named tuples (section_name, display_name, display_index)."""
        if not self._indexed_section_tuples:
            self.set_indexed_section_tuples()
        return self._indexed_section_tuples

    def set_section_name_list(self):
        self._section_name_list = [tpl.section_name for tpl in self.get_section_tuples()]

    def get_section_name_list(self):
        """Returns a list of section names."""
        if not self._section_name_list:
            self.set_section_name_list()
        return self._section_name_list

    def set_section_display_name_list(self):
        self._section_display_name_list = [tpl.display_name for tpl in self.get_section_tuples()]
        self._section_display_name_list.sort()

    def get_section_display_name_list(self):
        """Returns a list of section names to display."""
        if not self._section_display_name_list:
            self.set_section_display_name_list()
        return self._section_display_name_list

    def set_indexed_section_display_name_list(self):
        self._indexed_section_display_name_list = [tpl.display_name for tpl in self.get_indexed_section_tuples()]

    def get_indexed_section_display_name_list(self):
        """Returns a list of section names to display."""
        if not self._indexed_section_display_name_list:
            self.set_indexed_section_display_name_list()
        return self._indexed_section_display_name_list
