from bhp_site_edc import edc as admin
from bhp_section.models import Section


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'display_index')
admin.site.register(Section, SectionAdmin)
