from bhp_section.classes import section_index, section

app_name = 'bhp_section'  # settings.APP_NAME
section_index.setup()
urlpatterns = section.urlpatterns()
urlpatterns += section_index.urlpatterns()
