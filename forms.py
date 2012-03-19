from django import forms
from bhp_common.classes import MyModelForm
from lab_barcode.models import ZplTemplate, LabelPrinter


class LabelForm(forms.Form):
    
    identifier = forms.CharField(
        max_length=25,
        label="Identifier",
        help_text="",
        error_messages={'required': 'Please enter a valid identifier.'},
        #initial=""
        )


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
