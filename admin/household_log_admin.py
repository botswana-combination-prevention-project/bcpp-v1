from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_household.models import HouseholdLogEntry, HouseholdLog
from bcpp_household.forms import HouseholdLogForm, HouseholdLogEntryForm


class HouseholdLogEntryAdmin(BaseModelAdmin):
    form = HouseholdLogEntryForm
    date_hierarchy = 'modified'
    list_per_page = 15
    readonly_fields = ('household_log', )
    list_display = ('household_log', 'report_datetime', 'hbc', 'next_appt_datetime')
    list_filter = ('report_datetime', 'hbc', 'next_appt_datetime')
admin.site.register(HouseholdLogEntry, HouseholdLogEntryAdmin)


class HouseholdLogEntryInline(admin.TabularInline):
    model = HouseholdLogEntry
    extra = 1
    max_num = 5


class HouseholdLogAdmin(BaseModelAdmin):
    form = HouseholdLogForm
    inlines = [HouseholdLogEntryInline, ]
    date_hierarchy = 'modified'
    list_per_page = 15
    readonly_fields = ('household', 'survey')
    search_fields = ('household__household_identifier',)
    list_filter=('survey', 'hostname_created', 'created')
admin.site.register(HouseholdLog, HouseholdLogAdmin)
