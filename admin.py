from django.contrib import admin
from bhp_common.models import MyModelAdmin
from bhp_entry.admin import EntryInline
from bhp_visit.models import MembershipForm, ScheduleGroup, VisitDefinition


class MembershipFormAdmin (MyModelAdmin):
    pass
admin.site.register(MembershipForm, MembershipFormAdmin)


class ScheduleGroupAdmin(MyModelAdmin):
    #list_display = ('group_name', 'membership_form', 'grouping_key')
    pass
admin.site.register(ScheduleGroup, ScheduleGroupAdmin)    


class VisitDefinitionAdmin(MyModelAdmin):
    list_display = ('code', 'title', 'grouping', 'time_point', 'base_interval', 'base_interval_unit','lower_window', 'lower_window_unit', 'upper_window', 'upper_window_unit','user_modified', 'modified')
    
    search_fields = ('code', 'grouping',)
    
    inlines = [EntryInline,]
        
admin.site.register(VisitDefinition, VisitDefinitionAdmin)


