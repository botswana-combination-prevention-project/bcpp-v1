from django import forms
from bhp_common.classes import MyModelForm
from models import Link


# Link
class LinkForm (MyModelForm): 
    def clean(self):
    
        cleaned_data = self.cleaned_data 
        
        return super(LinkForm, self).clean()
        
    class Meta:
        model = Link
