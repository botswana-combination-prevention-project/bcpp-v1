from edc.lab.lab_requisition.forms import BaseRequisitionForm

from django import forms
from ..models import SubjectRequisition


class SubjectRequisitionForm(BaseRequisitionForm):

    def clean(self):
        cleaned_data = super(SubjectRequisitionForm, self).clean()
        panel = cleaned_data.get('panel')
        if panel:
            if panel.name in ['Research Blood Draw', 'Viral Load']:
                if (self.estimated_volume < 8.0 or self.estimated_volume > 10.0):
                    raise forms.ValidationError("The estimated volume should between 8.0 and 10.0 ml.")
            elif panel.name == 'Microtube':
                if (self.estimated_volume < 3.0 or self.estimated_volume > 5.0):
                    raise forms.ValidationError("The estimated volume should between 3.0 and 5.0 ml.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(SubjectRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    class Meta:
        model = SubjectRequisition
