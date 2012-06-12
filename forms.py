from django import forms
from bhp_base_form.classes import BaseModelForm
from models import Link


# Link
class LinkForm (BaseModelForm): 
    def clean(self):
    
        cleaned_data = self.cleaned_data 
        
        return super(LinkForm, self).clean()
        
    class Meta:
        model = Link
