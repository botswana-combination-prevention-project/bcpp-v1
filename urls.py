from bhp_section.classes import section_index_view, site_sections

section_index_view.setup()
urlpatterns = []
for site_section in site_sections.all().itervalues():
    site_section.section_list = section_index_view.get_section_list()
    urlpatterns += site_section().urlpatterns()
urlpatterns += section_index_view.urlpatterns()
