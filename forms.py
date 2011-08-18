from django import forms
from django.core.exceptions import ValidationError

class DescriberForm(forms.Form):
    
    app_label = forms.CharField(
        max_length=50, 
        label="App",
        required = False,
        #error_messages={'required': 'Please enter a valid app_label.'},
        )
    model_name = forms.CharField(
        max_length=50, 
        label="Model",
        required = False,        
        #error_messages={'required': 'Please enter a model name.'},
        )

