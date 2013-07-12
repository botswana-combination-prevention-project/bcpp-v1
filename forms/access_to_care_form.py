from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import AccessToCare


class AccessToCareForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        # if other, specify
        if cleaned_data.get('often_medicalcare') == 'OTHER' and not cleaned_data.get('often_medicalcare_other'):
            raise forms.ValidationError('if other medical care is used, specify the kind of medical care received')
        if cleaned_data.get('whereaccess') == 'Other, specify' and not cleaned_data.get('whereaccess_other'):
            raise forms.ValidationError('if medical access is \'OTHER\', provide the type of medical access obtained')

        return cleaned_data

    class Meta:
        model = AccessToCare
