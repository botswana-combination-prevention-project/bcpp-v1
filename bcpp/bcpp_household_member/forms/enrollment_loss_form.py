from django import forms
from bhp066.apps.bcpp.base_model_form import BaseModelForm

from ..models import EnrollmentLoss


class EnrollmentLossForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(EnrollmentLossForm, self).clean()
        if not cleaned_data.get('household_member').enrollment_checklist_completed:
            raise forms.ValidationError('Enrollment Checklist has not been completed. Please correct.')
        return cleaned_data

    class Meta:
        model = EnrollmentLoss
