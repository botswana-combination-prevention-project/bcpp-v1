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

#         requisition = RequisitionMetaData.objects.get(appointment=cleaned_data.get('clinic_visit').appointment,
#                                                       lab_entry=LabEntry.objects.get(requisition_panel__name='Research Blood Draw'))
#         if requisition:
#             estimated_volume = cleaned_data.get('estimated_volume', None)
#             if not estimated_volume == 10.0:
#                 raise forms.ValidationError('For RBD requisition, the VOLUME should be 10ml')

#         viral_load = RequisitionMetaData.objects.get(appointment=cleaned_data.get('clinic_visit').appointment,
#                                                       lab_entry=LabEntry.objects.get(requisition_panel__name='Viral Load'))
#         if viral_load:
#             estimated_volume = cleaned_data.get('estimated_volume', None)
#             if not estimated_volume == 5.0:
#                 raise forms.ValidationError('The VOLUME for VL should be 5.0 ml')

        return cleaned_data

    class Meta:
        model = ClinicRequisition
