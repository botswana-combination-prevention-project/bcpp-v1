from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_entry.admin import EntryInline
from bhp_lab_entry.admin import LabEntryInline
from bhp_visit.models import VisitDefinition


class VisitDefinitionAdmin(BaseModelAdmin):

    list_display = ('code', 'title', 'grouping', 'time_point', 'base_interval', 'base_interval_unit', 'lower_window', 'lower_window_unit', 'upper_window', 'upper_window_unit', 'user_modified', 'modified')

    list_filter = ('code', 'grouping', 'time_point', 'base_interval')

    search_fields = ('code', 'grouping', 'id',)

    inlines = [EntryInline, LabEntryInline, ]

admin.site.register(VisitDefinition, VisitDefinitionAdmin)
