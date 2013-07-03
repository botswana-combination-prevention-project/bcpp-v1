from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bhp_birt_reports.models import ReportParameter
from bhp_birt_reports.models import BaseReport
from bhp_birt_reports.actions import process_report

class ReportParameterAdmin(BaseModelAdmin):
    #form = HouseholdLogEntryForm
    list_per_page = 15
    list_display = ('parameter_name', 'parameter_type',)
    list_filter = ('parameter_name', 'parameter_type',)
    search_fields = ('parameter_name', 'parameter_type',)
admin.site.register(ReportParameter, ReportParameterAdmin)


class ReportParameterInline(admin.TabularInline):
    model = ReportParameter
    extra = 1
    max_num = 5


class BaseReportAdmin(BaseModelAdmin):
    #form = HouseholdLogForm
    inlines = [ReportParameterInline, ]
    list_per_page = 15
    search_fields = ('report_name',)
    list_display = ('report_name',)
    list_filter = ('report_name',)
    actions = [process_report, ]
admin.site.register(BaseReport, BaseReportAdmin)
