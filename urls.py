from bhp_section.classes import section_index_view, site_sections

#app_name = 'bhp_section'  # settings.APP_NAME
section_index_view.setup()
site_sections.autodiscover()
for section in site_sections.get_registry().itervalues():
    urlpatterns = section.urlpatterns()
urlpatterns += section_index_view.urlpatterns()
