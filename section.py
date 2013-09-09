from classes import BaseSectionView, site_sections


class SectionAppointmentView(BaseSectionView):
    section_name = 'appointments'
    section_display_name = 'Appointments'
    section_display_index = 110
    # section_template =

site_sections.register(SectionAppointmentView)


# class SectionLabView(BaseSectionView):
#     section_name = 'lab'
#     section_display_name = 'Labs'
#     section_display_index = 120
#     # section_template =
#
# site_sections.register(SectionLabView)


class SectionAdministrationView(BaseSectionView):
    section_name = 'administration'
    section_display_name = 'Administration'
    section_display_index = 140
    # section_template =

site_sections.register(SectionAdministrationView)
