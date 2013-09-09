from django.contrib import messages
from bhp_base_admin.utils import ModelExporter


def export_as_html(modeladmin, request, queryset, **kwargs):
    """ Flags specimen(s) as received and generates a globally
    specimen identifier."""
    model_exporter = ModelExporter()
    for qs in queryset:
        model_exporter.export(request, qs.code)

export_as_html.short_description = "Export as html"
