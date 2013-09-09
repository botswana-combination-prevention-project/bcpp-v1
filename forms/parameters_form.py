from django import forms
from bhp_birt_reports.models import BaseReport


class ParametersForm(forms.Form):
    def __init__(self, parameters):
        self.params = parameters
    
        
    reports = forms.ModelChoiceField(
        queryset=BaseReport.objects.all().order_by('report_name'),)
