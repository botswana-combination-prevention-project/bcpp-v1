from django import forms

class CurrentGpsForm(forms.Form):
    
    deg_south = forms.IntegerField(label='DS')
    min_south = forms.FloatField(label='MS')
    deg_east  = forms.IntegerField(label='DE')
    min_east  = forms.FloatField(label='ME')
