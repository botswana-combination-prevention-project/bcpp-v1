from django import forms
from django.db.models import Q
from bhp_lab_registration.models import SimpleConsent

class PatientForm(forms.ModelForm): 
    
    pass
    
    """
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        qset = (
            Q(patient=self.instance.pk) |
            Q(patient__isnull=True)
            )            
        wtf = SimpleConsent.objects.filter(qset);
        w = self.fields['simple_consent'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice))
        w.choices = choices
    """        
