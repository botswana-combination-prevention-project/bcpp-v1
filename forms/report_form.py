from django import forms
from bhp_birt_reports.models import BaseReport


class ReportForm(forms.Form):
    reports = forms.ModelChoiceField(
        queryset=BaseReport.objects.all().order_by('report_name'),)
