from django.contrib import admin
from bhp_base_model.classes import BaseModelAdmin
from lab_panel.models import Panel, PanelGroup, TidPanelMapping


class PanelAdmin(BaseModelAdmin):

    list_display = ('name', 'panel_group')

    search_fields = ['name', ]

    filter_horizontal = (
        'test_code',
        'aliquot_type',
        )

admin.site.register(Panel, PanelAdmin)


class PanelGroupAdmin(BaseModelAdmin):

    list_display = ('name',)

admin.site.register(PanelGroup, PanelGroupAdmin)


class TidPanelMappingAdmin(BaseModelAdmin):

    list_display = ('tid', 'panel', )

admin.site.register(TidPanelMapping, TidPanelMappingAdmin)
