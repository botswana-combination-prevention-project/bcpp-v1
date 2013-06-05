from bhp_section.models import Section as SectionModel


class BaseSection(object):

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

    def setup(self):
        """Adds sections to the Section model if they do not exist."""
        sections = []
        default_sections = self.get_default_sections()
        for default_section in default_sections:
            if default_section[self.NAME] not in self.get_section_name_list():
                sections.append(default_section)
        sections = self.get_section_list() + sections
        for section in sections:
            if not SectionModel.objects.filter(name=section[self.NAME]):
                SectionModel.objects.create(name=section[self.NAME], display_name=section[self.DISPLAY_NAME], display_index=section[self.DISPLAY_INDEX])
        self._set_section_lists()

    def _set_section_lists(self):
        """ Sets a list of sections that apply to this search class' urlpatterns."""
        self._section_list = [(section.name, section.display_name, section.display_index) for section in SectionModel.objects.filter(display=True).order_by('display_index')]
        self._section_name_list = [tpl[self.NAME] for tpl in self._section_list]
        self._section_display_name_list = [tpl[self.DISPLAY_NAME] for tpl in self._section_list]
        #self._section_name_list = list(set(self._section_name_list))
        #self._section_display_name_list = list(set(self._section_display_name_list))

    def get_section_list(self):
        if not self._section_list:
            self._set_section_lists()
        return self._section_list

    def get_section_name_list(self):
        if not self._section_name_list:
            self._set_section_lists()
        return self._section_name_list

    def get_section_display_name_list(self):
        if not self._section_display_name_list:
            self._set_section_lists()
        return self._section_display_name_list
