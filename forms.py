from django import forms
from django.contrib.admin.widgets import AdminRadioSelect, AdminRadioFieldRenderer
from bhp_common.classes import MyModelForm
from lab_barcode.models import ZplTemplate, LabelPrinter


# ZplTemplate
class ZplTemplateForm (MyModelForm): 
    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data
        
    class Meta:
        model = ZplTemplate

# LabelPrinter
class LabelPrinterForm (MyModelForm): 
    def clean(self):
    
        cleaned_data = self.cleaned_data 
    
        return cleaned_data
        
    class Meta:
        model = LabelPrinter
