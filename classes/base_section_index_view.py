from django.core.exceptions import ImproperlyConfigured
from controller import site_sections
from bhp_search.classes import site_search


class BaseSectionIndexView(object):

    """ Base section class. """

    NAME = 0
    DISPLAY_NAME = 1
    DISPLAY_INDEX = 2

    def __init__(self):
        """
        Keyword Arguments:
            search_result_template --
            section_name --
        """
        self._section_list = []
        self._section_name_list = []
        self._section_display_name_list = []
        self.selected_section = None
        self.is_setup = False

    def setup(self):
        if not self.is_setup:
            site_sections.autodiscover()
            self._set_section_list()
            site_search.autodiscover(self.get_section_list())
            self.is_setup = True

    def _set_section_list(self):
        """ Sets a list of sections that apply to this section class' urlpatterns."""
        #self._section_list = [(section.name, section.display_name, section.display_index) for section in SectionModel.objects.filter(display=True).order_by('display_index')]
        display_indexes = []
        unordered_section_list = []
        for site_section in site_sections.all().itervalues():
            unordered_section_list.append((site_section.section_name, site_section.section_display_name, site_section.section_display_index))
            display_indexes.append(site_section.section_display_index)
        # are display_indexes unique?
        if list(set(display_indexes)).sort() != display_indexes.sort():
            raise ImproperlyConfigured('Section classes must have a unique section_display_index. Got {0} from site_sections {1}. Check the section model in each app.'.format(display_indexes, site_sections.get_section_names()))
        display_indexes.sort()
        for index in display_indexes:
            for section_tpl in unordered_section_list:
                if section_tpl[self.DISPLAY_INDEX] == index:
                    self._section_list.append(section_tpl)
                    break
        self._section_name_list = [tpl[self.NAME] for tpl in self._section_list]
        self._section_display_name_list = [tpl[self.DISPLAY_NAME] for tpl in self._section_list]

    def get_section_list(self):
        """Returns a list of sections."""
        if not self._section_list:
            self._set_section_list()
        return self._section_list

    def get_section_name_list(self):
        """Returns a list of section names."""
        if not self._section_name_list:
            self._set_section_lists()
        return self._section_name_list

    def get_section_display_name_list(self):
        """Returns a list of section names to display."""
        #if not self._section_display_name_list:
        #    self._set_section_lists()
        return self._section_display_name_list
