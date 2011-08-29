from datetime import *
from django.contrib import admin
from bhp_common.models import MyModelAdmin, MyStackedInline
from autocomplete.views import autocomplete, AutocompleteSettings
from autocomplete.admin import AutocompleteAdmin
from bhp_lab_panel.models import Panel, PanelGroup, TidPanelMapping


class PanelAdmin(MyModelAdmin):

    list_display = ('name','panel_group')
    
    search_fields = ['name']
    
    filter_horizontal = (
        'test_code',
        'aliquot_type',
        'account',
        )
        
admin.site.register(Panel, PanelAdmin)


class PanelGroupAdmin(MyModelAdmin):

    list_display = ('name',)

admin.site.register(PanelGroup, PanelGroupAdmin)


class TidPanelMappingAdmin(MyModelAdmin):

    list_display = ('tid','panel')

admin.site.register(TidPanelMapping, TidPanelMappingAdmin)


