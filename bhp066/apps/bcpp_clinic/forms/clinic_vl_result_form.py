from django import forms

from edc.base.form.forms import BaseModelForm
from edc.constants import NEW
from edc.entry_meta_data.models import RequisitionMetaData
from edc.subject.entry.models import LabEntry

from ..models import ClinicVLResult


class ClinicVLResultForm (BaseModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        vl_requisition_metadata = RequisitionMetaData.objects.get(appointment=cleaned_data.get('clinic_visit').appointment, lab_entry=LabEntry.objects.get(requisition_panel__name='Viral Load (clinic)'))
        if vl_requisition_metadata.entry_status == NEW:
            raise forms.ValidationError('If a Viral Load Clinic Requisition is required, then you have to fill it before this form.')

        if cleaned_data.get('assay_date', None) <= cleaned_data.get('collection_datetime', None).date():
            raise forms.ValidationError('Assay date CANNOT be less than or equal to the date sample drawn. Please correct.')

        return cleaned_data

    class Meta:
        model = ClinicVLResult
