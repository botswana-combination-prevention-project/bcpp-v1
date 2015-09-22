from django import forms

from edc.lab.lab_requisition.forms import BaseRequisitionForm

from ..models import ClinicRequisition


class ClinicRequisitionForm(BaseRequisitionForm):

    def __init__(self, *args, **kwargs):
        super(ClinicRequisitionForm, self).__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        super(ClinicRequisitionForm, self).clean()
        cleaned_data = self.cleaned_data
        if cleaned_data.get('is_drawn', None) == 'Yes' and cleaned_data.get('item_type', None) != 'tube':
            raise forms.ValidationError('The item collection type should always be TUBE')
        return cleaned_data

    class Meta:
        model = ClinicRequisition
