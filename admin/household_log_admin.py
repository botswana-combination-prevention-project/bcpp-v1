from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_household.models import HouseholdLogEntry, HouseholdLog
from bcpp_household.forms import HouseholdLogForm, HouseholdLogEntryForm


class HouseholdLogEntryAdmin(BaseModelAdmin):
    form = HouseholdLogEntryForm
    date_hierarchy = 'modified'
    list_per_page = 15
    readonly_fields = ('household_log', )
    list_display = ('household_log', 'report_datetime', 'next_appt_datetime')
    list_filter = ('household_log__household_structure__survey', 'report_datetime', 'next_appt_datetime')
admin.site.register(HouseholdLogEntry, HouseholdLogEntryAdmin)


class HouseholdLogEntryInline(admin.TabularInline):
    model = HouseholdLogEntry
    extra = 0
    max_num = 5


class HouseholdLogAdmin(BaseModelAdmin):
    form = HouseholdLogForm
    inlines = [HouseholdLogEntryInline, ]
    date_hierarchy = 'modified'
    list_per_page = 15
    list_display = ('household_structure', 'structure', 'modified', 'user_modified', 'hostname_modified')
    readonly_fields = ('household_structure', )
    search_fields = ('household_structure__household__household_identifier', 'household_structure__pk')
    list_filter = ('household_structure__survey', 'hostname_created', 'created')
admin.site.register(HouseholdLog, HouseholdLogAdmin)
