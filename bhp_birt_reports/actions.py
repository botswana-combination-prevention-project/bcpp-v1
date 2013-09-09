from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template import RequestContext


def process_report(modeladmin, request, queryset, **kwargs):
    report_names = [rp.report_name for rp in queryset]
    if len(report_names) > 1:
        raise TypeError('Please select only one report at a time.')
    return HttpResponseRedirect("/bhp_birt_reports/report_parameters/?reports={0}".format(print_list(report_names)))
    
process_report.short_description = "Generate Report"

def print_list(report_names):
    comma_names = ""
    for name in report_names:
        if comma_names == "":
            comma_names = name
        else:
            comma_names = name +','+ comma_names 
    return comma_names
        